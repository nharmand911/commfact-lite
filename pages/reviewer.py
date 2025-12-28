import streamlit as st
from utils.auth import check_access, logout_handler
from core.decision import submit_decision
from core.content_store import get_content_queue
from audit.audit_logger import get_audit_log
from analytics.analytics_google import log_event_google

# =========================
# ACCESS GUARD
# =========================
check_access("Reviewer")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.subheader("👤 Session")
    st.caption(
        f"{st.session_state.get('username')} "
        f"({st.session_state.get('role')}) | "
        f"Agency: {st.session_state.get('agency_code')}"
    )

    st.divider()

    if st.button("Logout"):
        logout_handler()
        st.switch_page("app.py")

# =========================
# MAIN
# =========================
st.title("Review & Decision")
st.caption("Governance decision panel")

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
        f"{c['validation_result'].get('final_severity', 'N/A')}": i
        for i, c in enumerate(pending_contents)
    }

    selected_label = st.selectbox(
        "Select content to review",
        list(content_map.keys())
    )

    selected = pending_contents[content_map[selected_label]]

    # =========================
    # CONTENT DISPLAY (READ ONLY)
    # =========================
    st.subheader("📄 Content Under Review")
    st.text_area(
        "Content",
        value=selected.get("content", ""),
        height=220,
        disabled=True
    )

    # =========================
    # VALIDATION RESULT
    # =========================
    st.subheader("⚠️ Validation Result")
    severity = selected["validation_result"].get("final_severity", "N/A")

    if severity == "HIGH":
        st.error(f"Final Severity: {severity}")
    elif severity == "MEDIUM":
        st.warning(f"Final Severity: {severity}")
    else:
        st.info(f"Final Severity: {severity}")

    triggered_rules = selected["validation_result"].get("triggered_rules", [])

    if triggered_rules:
        st.warning("Triggered Rules:")
        for r in triggered_rules:
            st.write(f"- **{r.get('rule_id','')}**: {r.get('description','')}")
    else:
        st.success("✅ No rule violations detected")

    # =========================
    # DECISION
    # =========================
    st.divider()
    st.subheader("📝 Reviewer Decision")

    decision = st.selectbox(
        "Decision",
        ["REVISION_REQUIRED", "APPROVED"]
    )

    reason = st.text_area(
        "Decision Reason (Mandatory)",
        placeholder="Explain the decision and justification...",
        height=120
    )

    if st.button("Submit Decision", use_container_width=True):
        if not reason.strip():
            st.error("🚨 Decision reason is mandatory.")
        else:
            try:
                # --- Core decision ---
                submit_decision(
                    content=selected,
                    validation_result=selected["validation_result"],
                    decision=decision,
                    reason=reason,
                    actor_username=st.session_state.get("username"),
                    actor_role=st.session_state.get("role"),
                    agency_code=st.session_state.get("agency_code")
                )

                # --- Analytics ---
                log_event_google(
                    event_type="SUBMIT_DECISION",
                    object_type="DECISION",
                    object_id=selected["content_id"],
                    content_excerpt=selected["content"][:200],
                    severity=severity,
                    triggered_rules=", ".join(
                        [r["rule_id"] for r in triggered_rules]
                    ),
                    decision=decision,
                    app_version="v0.1-pilot"
                )

                st.success("✅ Decision recorded and content locked")
                st.rerun()

            except Exception as e:
                st.error(f"System error: {str(e)}")

# =========================
# AUDIT LOG (READ-ONLY)
# =========================
st.divider()
st.subheader("📜 Audit Log (Read-Only)")
st.caption("Permanent governance record")

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
    st.info("Audit log is empty.")
