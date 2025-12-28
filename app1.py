import streamlit as st
from core.validation import validate_content
from core.content import Content
from core.decision import submit_decision
from audit.audit_logger import AUDIT_LOG

st.set_page_config(page_title="COMMFACT Lite", layout="centered")

st.title("COMMFACT Lite")
st.caption("Communication Governance Validator")

# --- SECTION 1: CONTENT INPUT ---
st.subheader("1. Content Input")
content_text = st.text_area(
    "Paste content to be reviewed",
    height=200,
    placeholder="Enter caption, press release, or public statement here..."
)

# Global variable untuk menampung hasil validasi
validation_result = None

if content_text:
    validation_result = validate_content(content_text)

    # --- SECTION 2: AUTOMATED VALIDATION RESULT ---
    st.subheader("2. Validation Result")
    severity = validation_result["final_severity"]
    
    if severity == "HIGH":
        st.error(f"Final Severity: {severity}")
    elif severity == "MEDIUM":
        st.warning(f"Final Severity: {severity}")
    else:
        st.info(f"Final Severity: {severity}")

    if validation_result["triggered_rules"]:
        st.warning("Triggered Rules (Risk Detected):")
        for r in validation_result["triggered_rules"]:
            st.write(f"- **{r['rule_id']}**: {r['description']}")
    else:
        st.success("✅ No rule violations detected")

# --- SECTION 3: HUMAN REVIEWER DECISION ---
st.subheader("3. Reviewer Decision")

reviewer_role = "reviewer"  # Hardcoded for Lite MVP

decision = st.selectbox(
    "Decision",
    ["REVISION_REQUIRED", "APPROVED"]
)

reason = st.text_area(
    "Decision Reason (Mandatory)", 
    placeholder="Explain why this content is safe or why it needs revision..."
)

# SINGLE CONSOLIDATED BUTTON
if st.button("Submit Decision", key="final_submit", use_container_width=True):
    # GATE 1: Cek apakah ada konten
    if not content_text:
        st.error("Submission failed: No content provided.")
    
    # GATE 2: Cek apakah alasan diisi (Governance Metric: Decision reason > 90%)
    elif not reason.strip():
        st.error("🚨 GOVERNANCE BLOCK: You must provide a reason for your decision to maintain the audit trail.")
    
    # GATE 3: Proses jika semua syarat terpenuhi
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
            st.success(f"✅ Decision recorded in Audit Log: {decision}")
            # Opsional: st.balloons() untuk merayakan Zero-Error
        except Exception as e:
            st.error(f"System Error: {str(e)}")

# --- SECTION 4: AUDIT LOG ---
st.divider()
st.subheader("4. Audit Log (Read-Only)")
st.caption("This log is a permanent record for client accountability.")

if AUDIT_LOG:
    # Menampilkan log terbaru di atas
    for i, record in enumerate(reversed(AUDIT_LOG), 1):
        with st.expander(f"Record #{len(AUDIT_LOG)-i+1} - {record.get('decision')}"):
            st.json(record)
else:
    st.info("Audit log is currently empty.")
