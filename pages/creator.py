import streamlit as st
from utils.auth import check_access, logout_handler
from core.validation import validate_content
from core.content_store import add_content_to_queue

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
    st.subheader("👤 Session")
    st.caption(
        f"{st.session_state.get('username', '-')}"
        f" ({st.session_state.get('role', '-')}) | "
        f"Agency: {st.session_state.get('agency_code', '-')}"
    )

    st.divider()

    if st.button("Logout"):
        logout_handler()
        st.switch_page("app.py")

# =========================
# MAIN CONTENT
# =========================
st.title("Content Submission")
st.caption("Submit content for pre-publication risk validation")

content_text = st.text_area(
    "Paste content to be reviewed",
    height=200,
    placeholder="Enter caption, press release, or public statement...",
)

# =========================
# VALIDATION
# =========================
if content_text:
    validation_result = validate_content(content_text)

    st.subheader("Validation Result")

    severity = validation_result.get("final_severity", "LOW")
    triggered_rules = validation_result.get("triggered_rules", [])

    if severity == "HIGH":
        st.error(f"Final Severity: {severity}")
    elif severity == "MEDIUM":
        st.warning(f"Final Severity: {severity}")
    else:
        st.info(f"Final Severity: {severity}")

    if triggered_rules:
        st.warning("Triggered Rules:")
        for r in triggered_rules:
            st.write(f"- **{r.get('rule_id')}**: {r.get('description')}")
    else:
        st.success("✅ No rule violations detected")

    st.divider()

    # =========================
    # SUBMIT AREA
    # =========================
    notification_slot = st.empty()

    if st.session_state.get("submit_success"):
        notification_slot.success(
            "✅ Content successfully submitted to reviewer queue"
        )
        st.session_state["submit_success"] = False

    if st.button("📤 Submit for Review", use_container_width=True):
        # Save content
        record = add_content_to_queue(
            content_text=content_text,
            validation_result=validation_result,
            created_by=st.session_state.get("username"),
            agency_code=st.session_state.get("agency_code"),
        )

        # ✅ Analytics (single entry point)
        log_submit_content(
            content_id=record["content_id"],
            content_excerpt=content_text[:200],
            severity=severity,
            triggered_rules=", ".join(
                [r.get("rule_id", "") for r in triggered_rules]
            ),
        )

        st.session_state["submit_success"] = True
        st.rerun()
