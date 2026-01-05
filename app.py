import streamlit as st

from utils.session import init_session
from utils.auth import login_handler, logout_handler
from analytics.analytics_logger import log_event
from analytics.analytics_google import log_login, log_logout, log_event_google

from ui.ui_labels import UI   # ✅ UI LABELS

# =========================
# CONFIG
# =========================
TEST_MODE = True
DEFAULT_TEST_USER = "alice"
DEFAULT_TEST_ROLE = "Creator"
DEFAULT_TEST_AGENCY = "AGENCY-DEMO"

st.set_page_config(
    page_title=UI.APP_TITLE,
    layout="centered"
)

# =========================
# INIT SESSION
# =========================
init_session()

st.title(UI.APP_TITLE)
st.caption(UI.APP_SUBTITLE)
st.caption(UI.PILOT_WARNING)

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.get("logged_in"):

    st.subheader(UI.LOGIN_TITLE)

    username = st.text_input(
        UI.LOGIN_USERNAME,
        value=DEFAULT_TEST_USER if TEST_MODE else ""
    )

    role_selected = st.selectbox(
        UI.LOGIN_ROLE,
        UI.ROLES,
        index=0
    )

    agency_code = st.text_input(
        UI.LOGIN_AGENCY,
        value=DEFAULT_TEST_AGENCY if TEST_MODE else "",
        help=UI.LOGIN_AGENCY_HELP
    )

    if st.button(UI.LOGIN_BUTTON, use_container_width=True):
        success = login_handler(
            username=username,
            role_selected=role_selected,
            agency_code=agency_code
        )

        if success:
            log_event(
                event="LOGIN",
                object_type="USER_SESSION"
            )

            st.success(
                UI.LOGIN_SUCCESS.format(
                    username=username,
                    role=role_selected,
                    agency=agency_code
                )
            )
            st.rerun()
        else:
            st.error(UI.LOGIN_ERROR)

    st.stop()

# =========================
# SIDEBAR (GLOBAL)
# =========================
with st.sidebar:
    st.subheader(UI.SIDEBAR_SESSION)

    st.caption(
        UI.SIDEBAR_USER.format(
            username=st.session_state.get("username"),
            role=st.session_state.get("role")
        )
    )

    st.caption(
        UI.SIDEBAR_AGENCY.format(
            agency=st.session_state.get("agency_code")
        )
    )

    st.divider()

    if st.button(UI.LOGOUT_BUTTON):
        if st.session_state.get("logged_in"):
            log_event(
                event="LOGOUT",
                object_type="USER_SESSION"
            )

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

elif role == "Admin":
    st.switch_page("pages/analytics.py")

else:
    st.error(UI.INVALID_ROLE)
    logout_handler()
    st.switch_page("app.py")
