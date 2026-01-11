"""
COMMFACT Validation Orchestrator (Tier-0 Authority)
--------------------------------------------------
Responsibilities:
- Execute Tier-0 hard rules (non-configurable)
- Invoke Tier-1 rule engine (CSV-based)
- Aggregate violations
- Derive final severity (system-authoritative)

NON-RESPONSIBILITIES:
- UI interpretation
- Logging / audit
"""

from typing import Dict, List

from core.rule_engine import evaluate
from core.rule_loader import load_rules

# 🔒 Tier-0 hard rules (code-level)
from rules.rule_definitions import (
    AbsoluteClaimRule,
    GuaranteeClaimRule
)

# =========================================================
# LOAD TIER-1 RULES (CSV)
# =========================================================

RULES = load_rules("core/rules.csv")


# =========================================================
# PUBLIC API
# =========================================================

def validate_content(content: str, context: Dict | None = None) -> Dict:
    """
    Tier-0 validation entry point.

    Returns a system-authoritative validation result
    to be consumed by UI, audit, and decision layers.
    """

    context = context or {}

    # -----------------------------------------------------
    # STEP 1 — EXECUTE TIER-0 HARD RULES (FAIL-SAFE)
    # -----------------------------------------------------

    tier0_violations: List[Dict] = []

    for rule in (AbsoluteClaimRule(), GuaranteeClaimRule()):
        if rule.detect(content):
            tier0_violations.append({
                "rule_id": rule.rule_id,
                "category": rule.category,
                "severity": "HIGH",  # 🔒 forced
                "description": rule.description,
                "rationale": rule.rationale,
                "tier": "TIER_0"
            })

    # -----------------------------------------------------
    # STEP 2 — EXECUTE TIER-1 RULE ENGINE (CSV)
    # -----------------------------------------------------

    engine_result = evaluate(
        content=content,
        context=context,
        rules=RULES
    )

    tier1_violations = engine_result.get("violations", [])

    # -----------------------------------------------------
    # STEP 3 — MERGE VIOLATIONS (TIER-0 FIRST)
    # -----------------------------------------------------

    all_violations = tier0_violations + tier1_violations

    final_severity = _derive_final_severity(all_violations)

    # -----------------------------------------------------
    # STEP 4 — OVERRIDE DECISION UNTUK LGL-GUA-01
    # -----------------------------------------------------
    decision = engine_result.get("decision", "ALLOW")

    if any(r["rule_id"] == "LGL-GUA-01" for r in all_violations):
        decision = "STOP"

    return {
        "decision": decision,
        "score": engine_result.get("score"),
        "final_severity": final_severity,
        "triggered_rules": all_violations
    }

# =========================================================
# SEVERITY AGGREGATION (SYSTEM AUTHORITY)
# =========================================================

def _derive_final_severity(violations: List[Dict]) -> str:
    """
    Aggregate severities from triggered rules.

    Governance principles:
    - Tier-0 HIGH is absolute
    - Highest severity wins
    - No violation = LOW
    """

    if any(v.get("severity") == "HIGH" for v in violations):
        return "HIGH"

    if any(v.get("severity") == "MEDIUM" for v in violations):
        return "MEDIUM"

    return "LOW"
