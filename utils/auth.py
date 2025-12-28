import streamlit as st

# =====================================================
# Dummy user store (Tier 1 Pilot)
# =====================================================
DUMMY_USERS = {
    "alice": "Creator",
    "bob": "Reviewer"
}

def login_handler(username: str, role_selected: str, agency_code: str) -> bool:
    if not username or not role_selected or not agency_code:
        return False

    if username in DUMMY_USERS and DUMMY_USERS[username] == role_selected:
        st.session_state.update({
            "logged_in": True,
            "username": username,
            "role": role_selected,
            "agency_code": agency_code
        })
        return True

    return False


def logout_handler():
    for k in ["logged_in", "username", "role", "agency_code"]:
        st.session_state.pop(k, None)


def check_access(required_role: str):
    if not st.session_state.get("logged_in", False):
        st.error("⚠️ Please login first")
        st.stop()

    if st.session_state.get("role") != required_role:
        st.error("⛔ Access denied")
        st.stop()
