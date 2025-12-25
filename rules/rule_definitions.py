from rules.rule_base import Rule

class AbsoluteClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="BMC-01",
            category="Brand & Message Consistency",
            severity="MEDIUM",
            description="Detects absolute or total claims in content",
            rationale="Absolute claims may increase reputational and legal risk"
        )

    def detect(self, text: str) -> bool:
        keywords = [
            "100%",
            "tanpa risiko",
            "paling",
            "satu-satunya"
        ]
        return any(k.lower() in text.lower() for k in keywords)
