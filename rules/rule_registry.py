from rules.rule_definitions import (
    AbsoluteClaimRule,
    SuperiorityClaimRule,
    GuaranteeClaimRule
)

RULE_REGISTRY = [
    AbsoluteClaimRule(),
    SuperiorityClaimRule(),
    GuaranteeClaimRule()
]
