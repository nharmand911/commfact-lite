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
    validation_result = validate_content(content_text)

    severity = validation_result.get("final_severity", "LOW")
    triggered_rules = validation_result.get("triggered_rules", [])

    # =========================
    # DECISION SUMMARY (UI ONLY, advisory)
    # =========================
    st.divider()
    st.subheader("Validation Signal (System Advisory)")

    advisory_status = "STOP" if severity == "HIGH" else "FLAG" if severity == "MEDIUM" else "ALLOW"
#    content_excerpt = content_text.splitlines()[0][:100]  # 1 baris, max 100 chars

    st.markdown(
        f"### {UI.STATUS_ICONS.get(advisory_status,'')} "
        f"Validation Signal: {UI.STATUS_LABELS.get(advisory_status, advisory_status)}"
    )
#    st.markdown(f"### {UI.STATUS_ICONS.get(advisory_status,'')} Status (Advisory): {UI.STATUS_LABELS.get(advisory_status, advisory_status)}")
    st.markdown(f"**Tingkat Risiko (berdasarkan validasi sistem):** {UI.RISK_LABELS.get(severity, severity)}")

    if triggered_rules:
        st.markdown("**Indikasi pelanggaran terdeteksi:**")
        for rule_id in [r.get("rule_id") for r in triggered_rules][:3]:
            st.write(f"• {UI.RULE_LABELS.get(rule_id, rule_id)}")

#    if advisory_status in UI.ACTION_HINTS:
#        st.info(f"**Tindakan disarankan (Advisory):** {UI.ACTION_HINTS[advisory_status]}")

#    if content_excerpt:
#        st.markdown("**Cuplikan Konten:**")
#        st.text_area(
#            label="Cuplikan Konten",
#            value=content_excerpt,
#            height=50,
#            disabled=True
#        )

    st.caption(f"ℹ️ {UI.VALIDATION_DISCLAIMER}")

    st.divider()

    # =========================
    # SUBMIT AREA
    # =========================
    notification_slot = st.empty()
    if st.session_state.get("submit_success"):
        notification_slot.success(UI.SUBMIT_SUCCESS_MSG)
        st.session_state["submit_success"] = False

    if st.button(UI.SUBMIT_BUTTON, use_container_width=True):
        # Save content
        record = add_content_to_queue(
            content_text=content_text,
            validation_result=validation_result,
            created_by=st.session_state.get("username"),
            agency_code=st.session_state.get("agency_code"),
        )
        st.session_state["submit_success"] = True
        st.rerun()
