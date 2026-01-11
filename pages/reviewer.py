import streamlit as st
from utils.auth import check_access, logout_handler
from core.decision import submit_decision
from core.content_store import get_content_queue
from audit.audit_logger import get_audit_log
from analytics.analytics_google import log_event_google

from ui.ui_labels import UI  # ✅ gunakan class UI

# =========================
# ACCESS GUARD
# =========================
check_access("Reviewer")

# =========================
# SIDEBAR
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
# MAIN
# =========================
st.title(UI.REVIEW_TITLE)
st.caption(UI.REVIEW_CAPTION)

# =========================
# CONTENT QUEUE
# =========================
CONTENT_QUEUE = get_content_queue()
pending_contents = [c for c in CONTENT_QUEUE if c.get("status") == "SUBMITTED"]

if not pending_contents:
    st.info("📭 No content pending review.")
else:
    content_map = {
        f"{i+1}. {c.get('created_by')} — "
        f"{c['validation_result'].get('final_severity', 'N/A')}"
        : i
        for i, c in enumerate(pending_contents)
    }

    selected_label = st.selectbox(
        "Select content to review",
        list(content_map.keys())
    )
    selected = pending_contents[content_map[selected_label]]
    current_content_id = selected.get("content_id")


    # =========================
    # 🔑 RESET STATE JIKA PINDAH KONTEN
    # =========================
    if st.session_state.get("active_content_id") != current_content_id:
        st.session_state["active_content_id"] = current_content_id
        st.session_state["decision_submitted"] = False
        st.session_state.pop("decision_input", None)
        st.session_state.pop("reason_input", None)



    # =========================
    # STAGE 1: CONTENT & PRELIMINARY DECISION SUMMARY
    # =========================
    st.subheader(UI.CONTENT_UNDER_REVIEW)
    st.text_area(
        label="Content",
        value=selected.get("content", ""),
        height=220,
        disabled=True,
        key=f"content_display_{current_content_id}"
    )

    engine_result = selected.get("validation_result", {})

    # 🔐 IMMUTABLE ENGINE RESULT
    severity = engine_result.get("final_severity")
    triggered_rules = engine_result.get("triggered_rules", [])

    if severity is None:
        st.error("CRITICAL: Content has no immutable severity. Review blocked.")
        st.stop()

    decision = engine_result.get("decision", "N/A")
    score = engine_result.get("score", 0)
    violations = engine_result.get("violations", [])

    # =========================
    # VALIDATION RESULT
    # =========================

    st.subheader("⚠️ Validation Result")
    if severity == "HIGH":
        st.error(f"Final Severity: {severity}")
    elif severity == "MEDIUM":
        st.warning(f"Final Severity: {severity}")
    else:
        st.info(f"Final Severity: {severity}")
    if triggered_rules:
        st.warning(UI.TRIGGERED_RULES_LABEL)
        for r in triggered_rules:
            st.write(
                f"- **{UI.RULE_LABELS.get(r.get('rule_id'), r.get('rule_id'))}**: "
                f"{r.get('description','')}"
                f"{r.get('message','')}"
            )
    else:
        if severity in ("HIGH", "MEDIUM"):
            st.warning(
                "⚠️ Risiko terdeteksi berdasarkan evaluasi sistem secara keseluruhan, "
                "meskipun tidak ada satu pelanggaran tunggal yang berdiri sendiri."
            )
        else:
            st.success(UI.NO_RULE_VIOLATION)


    # =========================
    # PRELIMINARY DECISION SUMMARY (UI ONLY)
    # =========================
    st.divider()
    st.subheader("UI Preview")
    
    ui_risk_signal = (
        "STOP" if severity == "HIGH"
        else "FLAG" if severity == "MEDIUM"
        else "ALLOW"
    )
    
    st.session_state["decision_status"] = ui_risk_signal
    st.session_state["risk_level"] = severity
    st.session_state["triggered_rules"] = [r.get("rule_id") for r in triggered_rules]
    st.session_state["content_excerpt"] = selected.get("content", "").splitlines()[0][:100]

    st.markdown(
        f"### {UI.STATUS_ICONS.get(ui_risk_signal, '')} "
        f"System Risk Signal: {UI.STATUS_LABELS.get(ui_risk_signal, ui_risk_signal)}"
    )
#    st.markdown(
#        f"**Tingkat Risiko Terdeteksi:** "
#        f"{UI.RISK_LABELS.get(severity, severity)}"
#    )

    if st.session_state["triggered_rules"]:
        st.markdown("**Indikasi pola berisiko yang terdeteksi sistem:**")
        for r in triggered_rules:
            st.write(
                f"- **{UI.RULE_LABELS.get(r.get('rule_id'), r.get('rule_id'))}**: "
                f"{r.get('description','')}"
                f"{r.get('message','')}"
            )
#            st.write(f"• {r['rule_id']} – {UI.RULE_LABELS.get(r['rule_id'], '')}")

    st.caption(f"ℹ️ {UI.REVIEW_SUMMARY_DISCLAIMER}")

    # =========================
    # STAGE 2: INPUT DECISION
    # =========================
    if "decision_submitted" not in st.session_state:
        st.session_state["decision_submitted"] = False

    if not st.session_state["decision_submitted"]:
        st.divider()
        st.subheader(UI.REVIEWER_DECISION_TITLE)

        decision_input = st.selectbox(
            UI.DECISION_SELECT_LABEL,
            ["REVISION_REQUIRED", "APPROVED"],
            key=f"decision_input_{current_content_id}"
        )

        reason_input = st.text_area(
            "Decision Reason (Mandatory)",
            placeholder=UI.DECISION_REASON_PLACEHOLDER,
            height=120,
            key=f"decision_reason_{current_content_id}"
        )

        if st.button("Submit Decision", key=f"submit_{current_content_id}", use_container_width=True):
            if not reason_input.strip():
                st.error(UI.DECISION_REASON_ERROR)
            else:
                try:
                    submit_decision(
                        content=selected,
                        validation_result=engine_result,
                        decision=decision_input,
                        reason=reason_input,
                        actor_username=st.session_state.get("username"),
                        actor_role=st.session_state.get("role"),
                        agency_code=st.session_state.get("agency_code")
                    )
                    log_event_google(
                        event_type="SUBMIT_DECISION",
                        object_type="DECISION",
                        object_id=selected["content_id"],
                        content_excerpt=selected.get("content","")[:200],
                        severity=severity,
                        triggered_rules=", ".join(st.session_state["triggered_rules"]),
                        decision=decision_input,
                        app_version="v0.1-pilot"
                    )
                    st.session_state["decision_submitted"] = True
                    st.session_state["decision_input"] = decision_input
                    st.session_state["reason_input"] = reason_input
                    st.success(UI.DECISION_SUBMIT_SUCCESS)
                except Exception as e:
                    st.error(f"System error: {str(e)}")

    # =========================
    # STAGE 3: REVIEWER DECISION SUMMARY
    # =========================
    if st.session_state.get("decision_submitted"):
        st.divider()
        st.subheader("Reviewer Decision Summary (MVP Preview)")
        st.caption(
            "Tampilan ini adalah ringkasan UI untuk keperluan pilot. "
            "Bukan artefak keputusan sistem dan tidak dapat digunakan sebagai bukti formal."
        )      

        st.markdown(f"### {UI.STATUS_ICONS.get(ui_risk_signal, '')} Status: {UI.STATUS_LABELS.get(ui_risk_signal, ui_risk_signal)}")
        st.markdown(f"**Tingkat Risiko:** {UI.RISK_LABELS.get(severity, severity)}")
        st.markdown(f"**Keputusan Reviewer:** {st.session_state['decision_input']}")
        st.markdown(f"**Alasan Reviewer:** {st.session_state['reason_input']}")

        st.caption(
            "ℹ️ Ringkasan ini bersifat sementara dan hanya untuk membantu proses review manusia "
            "selama fase pilot. Artefak keputusan sistem akan tersedia pada fase produksi."
        )

# =========================
# AUDIT LOG (READ-ONLY)
# =========================
st.divider()
st.subheader(UI.AUDIT_LOG_TITLE)
st.caption(UI.AUDIT_LOG_CAPTION)

audit_log = get_audit_log()
if audit_log:
    for i, record in enumerate(reversed(audit_log), 1):
        with st.expander(
            f"Record #{len(audit_log)-i+1} — "
            f"{record.get('decision','N/A')} | "
            f"{record.get('actor','')} ({record.get('agency_code','')})"
        ):
            st.json(record)
else:
    st.info(UI.AUDIT_LOG_EMPTY)
