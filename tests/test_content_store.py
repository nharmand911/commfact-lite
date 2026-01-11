# test_content_store.py
import pytest
from core.content_store import add_content_to_queue

def test_audit_log_write_smoke():
    """
    UT-10 — Audit Log Write (Smoke Test)
    
    Tujuan:
        Pastikan proses penyimpanan record audit log tidak terputus.
    Assert:
        - Insert berhasil
        - record_hash terisi
    """
    content_text = "Konten uji untuk audit log smoke test"
    validation_result = {
        "decision": "ALLOW",
        "score": 0,
        "final_severity": "LOW",
        "triggered_rules": []
    }
    created_by = "tester"
    agency_code = "AGENCY-01"
    
    # Panggil fungsi penyimpanan
    record = add_content_to_queue(
        content_text=content_text,
        validation_result=validation_result,
        created_by=created_by,
        agency_code=agency_code
    )
    
    # =========================
    # ASSERTS
    # =========================
    
    # Fungsi tidak crash → record harus dict
    assert isinstance(record, dict), "add_content_to_queue harus mengembalikan dict"
    
    # record_hash ada dan tidak kosong
    assert "record_hash" in record, "record_hash harus ada di record"
    assert record["record_hash"], "record_hash tidak boleh kosong"
    
    # Optional: decision tersimpan sama dengan input
    assert record.get("validation_result", {}).get("decision") == "ALLOW", \
        "Decision di record harus sama dengan input"
