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
