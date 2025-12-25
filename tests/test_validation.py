from core.validation import validate_content

def test_high_severity_aggregation():
    result = validate_content("dijamin berhasil 100%")
    assert result["final_severity"] == "HIGH"

def test_no_rule_triggered():
    result = validate_content("produk ini aman")
    assert result["final_severity"] == "NONE"
