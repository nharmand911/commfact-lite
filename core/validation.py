from rules.rule_registry import RULE_REGISTRY
from config.constants import SEVERITY_LEVELS

def validate_content(text: str) -> dict:
    triggered_rules = []

    for rule in RULE_REGISTRY:
        if rule.detect(text):
            triggered_rules.append({
                "rule_id": rule.rule_id,
                "category": rule.category,
                "severity": rule.severity,
                "description": rule.description,
                "rationale": rule.rationale
            })

    final_severity = summarize_severity(triggered_rules)

    return {
        "final_severity": final_severity,
        "triggered_rules": triggered_rules
    }

def summarize_severity(triggered_rules: list) -> str:
    severities = {r["severity"] for r in triggered_rules}

    if "HIGH" in severities:
        return "HIGH"
    if "MEDIUM" in severities:
        return "MEDIUM"
    if "LOW" in severities:
        return "LOW"
    return "NONE"
