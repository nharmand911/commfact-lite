from rules.rule_definitions import (
    AbsoluteClaimRule,
    SuperiorityClaimRule,
    GuaranteeClaimRule
)

def test_absolute_claim():
    assert AbsoluteClaimRule().detect("100% aman")

def test_superiority_claim():
    assert SuperiorityClaimRule().detect("produk terbaik")

def test_guarantee_claim():
    assert GuaranteeClaimRule().detect("dijamin berhasil")
