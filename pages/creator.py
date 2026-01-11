import streamlit as st
from utils.auth import check_access, logout_handler
from core.validation import validate_content
from core.content_store import add_content_to_queue
from ui.ui_labels import UI  # ✅ gunakan class UI

# =========================
# ACCESS GUARD
# =========================
check_access("Creator")

# =========================
# SESSION FLAGS
# =========================
if "submit_success" not in st.session_state:
    st.session_state["submit_success"] = False

# =========================
# SIDEBAR (SESSION INFO)
# =========================
with st.sidebar:
    st.subheader(UI.SIDEBAR_SESSION)
    st.caption(
        f"{st.session_state.get('username', '-')}" 
        f" ({st.session_state.get('role', '-')}) | "
        f"Agency: {st.session_state.get('agency_code', '-')}"
    )
    st.divider()
    if st.button(UI.LOGOUT_BUTTON):
        logout_handler()
        st.switch_page("app.py")

# =========================
# MAIN CONTENT
# =========================
st.title(UI.CONTENT_SUBMISSION_TITLE)
st.caption(UI.CONTENT_SUBMISSION_CAPTION)

content_text = st.text_area(
    UI.CONTENT_PLACEHOLDER,
    height=200,
)


# =========================
# VALIDATION
# =========================
if content_text:
    validation_result = validate_content(content=content_text)

    decision = validation_result.get("decision", "ALLOW")
    severity = validation_result.get("final_severity", "LOW")
    triggered_rules = validation_result.get("triggered_rules", [])

    # =========================
    # VALIDATION SIGNAL (UI ONLY — NOT A DECISION)
    # =========================
    st.divider()
    st.subheader("UI Preview")

    # Gunakan decision dari rule engine
    st.markdown(
        f"### {UI.STATUS_ICONS.get(decision,'')} "
        f"Validation Signal: {UI.STATUS_LABELS.get(decision, decision)}"
    )

    # Tampilkan tingkat risiko sistem    
    st.markdown(
        f"**Tingkat Risiko (berdasarkan validasi sistem):** "
        f"{UI.RISK_LABELS.get(severity, severity)}"
    )

    if triggered_rules:
        st.markdown("**Indikasi pola berisiko yang terdeteksi sistem::**")
        for r in triggered_rules:
            st.write(
                f"- **{UI.RULE_LABELS.get(r.get('rule_id'), r.get('rule_id'))}**: "
                f"{r.get('description','')} {r.get('message','')}"
            )

    # =========================
    # UX GOVERNANCE NOTE (ALLOW + HIGH RISK)
    # =========================
    if decision == "ALLOW" and severity == "HIGH":
        st.info(UI.ALLOW_WITH_RISK_NOTE)

    st.caption(f"ℹ️ {UI.VALIDATION_DISCLAIMER}")

    # =========================
    # SPECIAL RULE HANDLING (STOP/REJECT)
    # =========================
    submit_disabled = False

    high_risk_rules = [r["rule_id"] for r in triggered_rules if r.get("severity") == "HIGH"]

    # LGL-ABS-01 → advisory HIGH risk, submit tetap boleh
    if "LGL-ABS-01" in high_risk_rules:
        st.info("⚠️ Konten mengandung klaim absolut (LGL-ABS-01). Periksa risiko sebelum submit.")

    # Tombol submit disable jika decision STOP/REJECT atau LGL-GUA-01
    if decision in ["STOP", "REJECT"] or "LGL-GUA-01" in high_risk_rules:
        submit_disabled = True
        if "LGL-GUA-01" in high_risk_rules:
            st.warning("❌ Konten mengandung klaim jaminan hasil pasti (LGL-GUA-01). Tidak bisa dikirim.")
          
    # Tombol submit tetap disable jika decision STOP/REJECT
    if decision in ["STOP", "REJECT"]:
        submit_disabled = True

    # =========================
    # SUBMIT AREA
    # =========================
    st.divider()    
    notification_slot = st.empty()
    if st.session_state.get("submit_success"):
        notification_slot.success(UI.SUBMIT_SUCCESS_MSG)
        st.session_state["submit_success"] = False

    submit_slot = st.empty()
    if submit_slot.button(UI.SUBMIT_BUTTON, use_container_width=True, disabled=submit_disabled):
        # Simpan konten
        add_content_to_queue(
            content_text=content_text,
            validation_result=validation_result,
            created_by=st.session_state.get("username"),
            agency_code=st.session_state.get("agency_code"),
        )
        st.session_state["submit_success"] = True
        st.rerun()
