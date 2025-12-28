class Rule:
    def __init__(
        self,
        rule_id: str,
        category: str,
        severity: str,
        description: str,
        rationale: str
    ):
        self.rule_id = rule_id
        self.category = category
        self.severity = severity
        self.description = description
        self.rationale = rationale

    def detect(self, text: str) -> bool:
        """
        Return True if the rule is triggered by the content.
        """
        raise NotImplementedError("Rule detection not implemented")
