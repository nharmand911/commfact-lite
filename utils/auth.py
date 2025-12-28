import streamlit as st

# =====================================================
# Dummy user store (Tier 1 Pilot)
# username : role
# =====================================================
DUMMY_USERS = {
    "alice": "Creator",
    "bob": "Reviewer"
}

def login_handler(username: str, role_selected: str, agency_code: str) -> bool:
    """
    Handle login logic.
    Returns True if login successful, False otherwise.
    Sets session state variables including agency_code.
    """
    # -----------------------
    # Basic validation
    # -----------------------
    if not username or not role_selected or not agency_code:
        return False

    # -----------------------
    # Dummy auth check
    # -----------------------
    if username in DUMMY_USERS and DUMMY_USERS[username] == role_selected:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = role_selected
        st.session_state["agency_code"] = agency_code
        return True

    return False


def logout_handler():
    """
    Clear session state and logout user.
    """
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.session_state["agency_code"] = None


def check_access(required_role: str):
    """
    Block access if user is not logged in or role mismatch.
    Redirects to app.py if not logged in.
    """
    if not st.session_state.get("logged_in"):
        st.warning("⚠️ Please login first")
        st.switch_page("app.py")

    if st.session_state.get("role") != required_role:
        st.error("⛔ Access denied")
        st.stop()
