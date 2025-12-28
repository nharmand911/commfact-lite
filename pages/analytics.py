import streamlit as st
import pandas as pd
from utils.auth import check_access, logout_handler
from audit.audit_logger import get_audit_log
from collections import Counter

# =========================
# ACCESS GUARD
# =========================
check_access("Reviewer")  # atau Admin di masa depan

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.subheader("👤 Session")
    st.caption(
        f"{st.session_state.get('username')} "
        f"({st.session_state.get('role')})"
    )
    st.divider()
    if st.button("Logout"):
        logout_handler()
        st.switch_page("app.py")

# =========================
# MAIN
# =========================
st.title("Agency Usage Dashboard")
st.caption("Internal governance analytics (pilot)")

# Ambil log audit
audit_log = get_audit_log()

if not audit_log:
    st.info("No audit data available yet.")
    st.stop()

# =========================
# Convert log ke DataFrame
# =========================
df = pd.DataFrame(audit_log)

# =========================
# FILTERS
# =========================
st.subheader("Filters")

agency_list = ["ALL"] + sorted(df["agency_code"].dropna().unique().tolist())
selected_agency = st.selectbox("Select Agency", agency_list)

decision_list = ["ALL"] + sorted(df["decision"].dropna().unique().tolist())
selected_decision = st.selectbox("Select Decision", decision_list)

filtered_df = df.copy()
if selected_agency != "ALL":
    filtered_df = filtered_df[filtered_df["agency_code"] == selected_agency]
if selected_decision != "ALL":
    filtered_df = filtered_df[filtered_df["decision"] == selected_decision]

# =========================
# AGENCY ACTIVITY CHART
# =========================
st.subheader("Agency Activity")
agency_counter = Counter(filtered_df["agency_code"].fillna("UNKNOWN"))
st.bar_chart(agency_counter)

# =========================
# DECISION BREAKDOWN CHART
# =========================
st.subheader("Decision Breakdown")
decision_counter = Counter(filtered_df["decision"].fillna("UNKNOWN"))
st.bar_chart(decision_counter)

# =========================
# RAW AUDIT LOG
# =========================
st.subheader("Raw Audit Log (Filtered)")
st.caption("Append-only governance record")
st.dataframe(filtered_df)

# =========================
# DOWNLOAD CSV
# =========================
st.subheader("Export CSV")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Audit Log as CSV",
    data=csv,
    file_name="audit_log.csv",
    mime="text/csv"
)
