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

class SuperiorityClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="BMC-02",
            category="Brand & Message Consistency",
            severity="MEDIUM",
            description="Detects superiority or comparison claims",
            rationale="Comparative superiority claims increase reputational risk"
        )

    def detect(self, text: str) -> bool:
        keywords = [
            "terbaik",
            "nomor satu",
            "lebih unggul",
            "paling direkomendasikan"
        ]
        return any(k.lower() in text.lower() for k in keywords)

class GuaranteeClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="LGL-01",
            category="Legal & Compliance",
            severity="HIGH",
            description="Detects explicit guarantee or certainty claims",
            rationale="Guarantee claims may expose legal liability"
        )

    def detect(self, text: str) -> bool:
        keywords = [
            "pasti berhasil",
            "dijamin",
            "tanpa kegagalan",
            "jaminan uang kembali"
        ]
        return any(k.lower() in text.lower() for k in keywords)

