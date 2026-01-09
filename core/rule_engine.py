"""
COMMFACT Rule Engine
-------------------
Pure deterministic rule evaluation engine.

Responsibilities:
- Evaluate content against policy rules
- Aggregate violations
- Compute total risk score
- Derive final decision

NON-RESPONSIBILITIES:
- Loading rules from file
- Logging / auditing
- UI rendering
- ACK construction
"""

from typing import List, Dict


# =========================================================
# CONFIGURATION (LOCKED FOR MVP TIER 1)
# =========================================================

REJECT_THRESHOLD = 70
REVIEW_THRESHOLD = 1  # any violation below reject threshold


# =========================================================
# CORE ENGINE
# =========================================================

def evaluate(content: str, context: Dict, rules: List[Dict]) -> Dict:
    """
    Evaluate content against a list of rules.

    Args:
        content (str): Communication content to be validated
        context (dict): Context metadata (brand, channel, sector, etc.)
        rules (list[dict]): Rule definitions

    Returns:
        dict: {
            "decision": "ALLOW|REVIEW|REJECT",
            "score": int,
            "violations": list[dict]
        }
    """

    # Defensive normalization (MVP level)
    content = content or ""
    content_lower = content.lower()

    total_score = 0
    violations = []

    for rule in rules:
        pattern = rule.get("pattern")
        rule_score = int(rule.get("score", 0))

        if not pattern:
            # Skip invalid rule silently (rule_loader should catch this)
            continue

        # Deterministic pattern match (NO NLP, NO REGEX by default)
        if pattern.lower() in content_lower:
            violation = {
                "rule_id": rule.get("rule_id"),
                "severity": rule.get("severity"),
                "message": rule.get("message")
            }
            violations.append(violation)
            total_score += rule_score

    decision = _derive_decision(total_score)

    return {
        "decision": decision,
        "score": total_score,
        "violations": violations
    }


# =========================================================
# DECISION LOGIC (ISOLATED & TESTABLE)
# =========================================================

def _derive_decision(score: int) -> str:
    """
    Determine final decision based on aggregated score.

    Decision rules:
    - score >= REJECT_THRESHOLD → REJECT
    - score >= REVIEW_THRESHOLD → REVIEW
    - score == 0 → ALLOW
    """

    if score >= REJECT_THRESHOLD:
        return "REJECT"
    elif score >= REVIEW_THRESHOLD:
        return "REVIEW"
    else:
        return "ALLOW"
