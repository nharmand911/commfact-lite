import streamlit as st

st.set_page_config(page_title="COMMFACT Lite", layout="centered")

st.title("COMMFACT Lite")
st.caption("Communication Governance Validator")

from core.validation import validate_content

st.subheader("1. Content Input")

content_text = st.text_area(
    "Paste content to be reviewed",
    height=200
)

if content_text:
    validation_result = validate_content(content_text)

    st.subheader("2. Validation Result")

    st.write("Final Severity:", validation_result["final_severity"])

    if validation_result["triggered_rules"]:
        st.warning("Triggered Rules:")
        for r in validation_result["triggered_rules"]:
            st.write(f"- {r['rule_id']}: {r['description']}")
    else:
        st.success("No rule violations detected")

from core.content import Content
from core.decision import submit_decision

st.subheader("3. Reviewer Decision")

reviewer_role = "reviewer"  # hardcoded for Lite MVP

decision = st.selectbox(
    "Decision",
    ["REVISION_REQUIRED", "APPROVED"]
)

reason = st.text_input(
    "Decision Reason (mandatory)"
)

if st.button("Submit Decision"):
    if not content_text:
        st.error("No content provided")
    else:
        content = Content(content_text, created_by="ui_user")

        try:
            submit_decision(
                content=content,
                validation_result=validation_result,
                decision=decision,
                reason=reason,
                user_role=reviewer_role
            )
            st.success(f"Decision recorded: {decision}")
        except Exception as e:
            st.error(str(e))

from audit.audit_logger import AUDIT_LOG

st.subheader("4. Audit Log (Read-Only)")

if AUDIT_LOG:
    for i, record in enumerate(AUDIT_LOG, 1):
        with st.expander(f"Decision #{i}"):
            st.json(record)
else:
    st.info("No audit records yet")

if st.button("Submit Decision"):
    if not reason.strip():
        st.error("Decision reason is required")
        st.stop()




