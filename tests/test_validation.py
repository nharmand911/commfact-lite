# test_validation.py
import pytest
from core.validation import validate_content

def test_missing_context_field():
    """
    UT-08 — Missing Context Field

    Input:
        context = {}
    Expected:
        - Tidak crash
        - Decision tetap keluar (ALLOW/REVIEW/STOP/REJECT)
        - Violations list tersedia
    """
    content = "Ini adalah konten uji untuk klaim absolut."
    context = {}  # context kosong
    
    # Panggil fungsi validate_content
    result = validate_content(content=content, context=context)
    
    # =========================
    # ASSERTS
    # =========================
    
    # Fungsi tidak crash → result harus dict
    assert isinstance(result, dict), "validate_content harus mengembalikan dict"
    
    # Decision ada dan valid
    assert "decision" in result, "Decision harus ada di result"
    assert result["decision"] in ["ALLOW", "REVIEW", "STOP", "REJECT"], \
        f"Decision unexpected: {result['decision']}"
    
    # Score tetap ada
    assert "score" in result, "Score harus ada di result"
    assert isinstance(result["score"], int), "Score harus berupa integer"
    
    # Violations ada (boleh kosong)
    assert "triggered_rules" in result, "Triggered rules harus ada di result"
    assert isinstance(result["triggered_rules"], list), "Triggered rules harus list"
    
    # Final severity ada
    assert "final_severity" in result, "Final severity harus ada di result"
    assert result["final_severity"] in ["LOW", "MEDIUM", "HIGH"], \
        f"Final severity unexpected: {result['final_severity']}"
