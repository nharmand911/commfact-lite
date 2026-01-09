import random
import copy
import pytest

from core.rule_engine import evaluate


# =========================================================
# FIXTURES (MINIMAL & EXPLICIT)
# =========================================================

@pytest.fixture
def base_context():
    return {
        "brand": "TestBrand",
        "channel": "Instagram",
        "sector": "Healthcare"
    }


@pytest.fixture
def simple_rules():
    return [
        {
            "rule_id": "ABS-CLAIM-001",
            "pattern": "100%",
            "severity": "CRITICAL",
            "score": 50,
            "message": "Absolute claim detected"
        },
        {
            "rule_id": "SUP-CLAIM-002",
            "pattern": "paling",
            "severity": "HIGH",
            "score": 30,
            "message": "Superiority claim detected"
        }
    ]


# =========================================================
# UT-01 — BASIC SANITY CHECK
# =========================================================

def test_ut01_basic_evaluation_structure(base_context, simple_rules):
    content = "Produk ini 100% paling aman."

    result = evaluate(content, base_context, simple_rules)

    assert isinstance(result, dict)
    assert "decision" in result
    assert "score" in result
    assert "violations" in result

    assert isinstance(result["violations"], list)
    assert result["decision"] in ["ALLOW", "REVIEW", "REJECT"]


# =========================================================
# UT-03 — DETERMINISM REPEATABILITY (CRITICAL)
# =========================================================

def test_ut03_determinism_repeatability(base_context, simple_rules):
    content = "Produk ini 100% paling aman."

    results = [
        evaluate(content, base_context, simple_rules)
        for _ in range(100)
    ]

    first = results[0]

    for r in results:
        assert r["decision"] == first["decision"]
        assert r["score"] == first["score"]
        assert r["violations"] == first["violations"]


# =========================================================
# UT-04 — RULE ORDER INDEPENDENCE
# =========================================================

def test_ut04_rule_order_independence(base_context, simple_rules):
    content = "Produk ini 100% paling aman."

    baseline = evaluate(content, base_context, simple_rules)

    shuffled_rules = copy.deepcopy(simple_rules)
    random.shuffle(shuffled_rules)

    shuffled_result = evaluate(content, base_context, shuffled_rules)

    assert baseline["decision"] == shuffled_result["decision"]
    assert baseline["score"] == shuffled_result["score"]

    # violations boleh beda urutan, tapi harus sama secara isi
    assert sorted(baseline["violations"], key=lambda x: x["rule_id"]) == \
           sorted(shuffled_result["violations"], key=lambda x: x["rule_id"])


# =========================================================
# UT-05 — THRESHOLD EDGE TEST
# =========================================================

def test_ut05_threshold_edge_review_vs_reject(base_context):
    content = "Produk ini dijamin aman."

    rules_review = [
        {
            "rule_id": "GEN-CLAIM-001",
            "pattern": "dijamin",
            "severity": "MEDIUM",
            "score": 69,
            "message": "Guarantee claim detected"
        }
    ]

    rules_reject = [
        {
            "rule_id": "GEN-CLAIM-002",
            "pattern": "dijamin",
            "severity": "HIGH",
            "score": 70,
            "message": "Guarantee claim detected"
        }
    ]

    result_review = evaluate(content, base_context, rules_review)
    result_reject = evaluate(content, base_context, rules_reject)

    assert result_review["score"] == 69
    assert result_review["decision"] == "REVIEW"

    assert result_reject["score"] == 70
    assert result_reject["decision"] == "REJECT"


# =========================================================
# UT-06 — MULTI-VIOLATION AGGREGATION
# =========================================================

def test_ut06_multi_violation_aggregation(base_context, simple_rules):
    content = "Produk ini 100% paling aman."

    result = evaluate(content, base_context, simple_rules)

    assert len(result["violations"]) == 2
    assert result["score"] == 80  # 50 + 30
    assert result["decision"] == "REJECT"


# =========================================================
# UT-07 — EMPTY CONTENT SAFETY (MVP LEVEL)
# =========================================================

def test_ut07_empty_content_safe(base_context, simple_rules):
    content = ""

    result = evaluate(content, base_context, simple_rules)

    assert "decision" in result
    assert "score" in result
    assert isinstance(result["violations"], list)
    assert result["decision"] in ["ALLOW", "REVIEW", "REJECT"]


# =========================================================
# UT-08 — MISSING CONTEXT SAFETY
# =========================================================

def test_ut08_missing_context_safe(simple_rules):
    content = "Produk ini 100% aman."
    context = {}

    result = evaluate(content, context, simple_rules)

    assert "decision" in result
    assert "score" in result
    assert isinstance(result["violations"], list)


# =========================================================
# FINAL NOTE
# =========================================================
# Jika salah satu test determinisme (UT-03 / UT-04) flaky,
# STOP. Jangan lanjut ke UI, ACK builder, atau audit log.
