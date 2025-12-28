import streamlit as st
from uuid import uuid4

# =====================================================
# Dummy user store (Tier 1 Pilot)
# username : role
# =====================================================
DUMMY_USERS = {
    "alice": "Creator",
    "bob": "Reviewer",
}

def login_handler(username: str, role_selected: str, agency_code: str) -> bool:
    """
    Handle login logic.
    Returns True if login successful, False otherwise.
    Sets ALL required session state for analytics & access control.
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

        # 🔑 REQUIRED for analytics
        st.session_state["session_id"] = str(uuid4())

        # 🔑 Analytics: login event
        try:
            from analytics.analytics_google import log_login
            log_login()
        except Exception as e:
            print(f"[Auth] log_login failed: {e}")

        return True

    return False


def logout_handler():
    """
    Clear session state and logout user.
    """

    # 🔑 Analytics: logout event (best effort)
    try:
        from analytics.analytics_google import log_logout
        log_logout()
    except Exception as e:
        print(f"[Auth] log_logout failed: {e}")

    # Clear all known session keys
    for key in [
        "logged_in",
        "username",
        "role",
        "agency_code",
        "session_id",
    ]:
        if key in st.session_state:
            del st.session_state[key]


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
