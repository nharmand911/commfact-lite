import streamlit as st
from utils.session import init_session
from utils.auth import login_handler, logout_handler
from analytics.analytics_logger import log_event  # 🔑 logging pilot
from analytics.analytics_google import log_login, log_logout  # 🔑 logging Google Sheet
from analytics.analytics_google import log_event_google # 🔑 logging Google Sheet

# =========================
# CONFIG
# =========================
TEST_MODE = True              # 🔧 matikan di production
DEFAULT_TEST_USER = "alice"
DEFAULT_TEST_ROLE = "Creator"
DEFAULT_TEST_AGENCY = "AGENCY-DEMO"

st.set_page_config(
    page_title="COMMFACT Lite",
    layout="centered"
)

# =========================
# INIT SESSION
# =========================
init_session()

st.title("COMMFACT Lite")
st.caption("Communication Governance Validator")
st.caption("⚠️ Pilot Version – Governance Simulation Only")

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.get("logged_in"):

    st.subheader("Login")

    username = st.text_input(
        "Username",
        value=DEFAULT_TEST_USER if TEST_MODE else ""
    )

    role_selected = st.selectbox(
        "Role",
        ["Creator", "Reviewer"],
        index=0 if TEST_MODE else 0
    )

    agency_code = st.text_input(
        "Agency Code",
        value=DEFAULT_TEST_AGENCY if TEST_MODE else "",
        help="Digunakan untuk analitik dan audit per agency"
    )

    if st.button("Login", use_container_width=True):
        success = login_handler(
            username=username,
            role_selected=role_selected,
            agency_code=agency_code
        )

        if success:
            # =========================
            # LOG LOGIN EVENT
            # =========================
            log_event(
                event="LOGIN",
                object_type="USER_SESSION"
            )

            #log_event_google(
            #   event_type="LOGIN",
            #    object_type="SESSION",
            #    object_id="",
            #    content_excerpt="",
            #    severity="",
            #    triggered_rules="",
            #    decision="",
            #    app_version="v0.1-pilot"
            #)

            # log_login()  # Google Sheet log

            st.success(
                f"Logged in as {username} "
                f"({role_selected}) – {agency_code}"
            )
            st.rerun()
        else:
            st.error("Invalid login credentials")

    st.stop()

# =========================
# SIDEBAR (GLOBAL)
# =========================
with st.sidebar:
    st.subheader("👤 Session")
    st.caption(
        f"{st.session_state.get('username')} "
        f"({st.session_state.get('role')})"
    )
    st.caption(
        f"🏢 Agency: {st.session_state.get('agency_code')}"
    )

    st.divider()

    if st.button("Logout"):
        if st.session_state.get("logged_in"):
            # =========================
            # LOG LOGOUT EVENT
            # =========================
            log_event(
                event="LOGOUT",
                object_type="USER_SESSION"
            )
            
            #log_event_google(
            #    event_type="LOGOUT",
            #    object_type="SESSION",
            #    object_id="",
            #    content_excerpt="",
            #    severity="",
            #    triggered_rules="",
            #    decision="",
            #    app_version="v0.1-pilot"
            #)
            
            # log_logout()  # Google Sheet log

        logout_handler()
        st.switch_page("app.py")

# =========================
# ROLE ROUTING
# =========================
role = st.session_state.get("role")

if role == "Creator":
    st.switch_page("pages/creator.py")

elif role == "Reviewer":
    st.switch_page("pages/reviewer.py")

elif role == "Admin":  # optional future
    st.switch_page("pages/analytics.py")

else:
    st.error("Invalid role in session.")
    logout_handler()
    st.switch_page("app.py")
