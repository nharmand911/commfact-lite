import streamlit as st

def init_session():
    """
    Initialise required session state variables.
    Must be called once at app startup.
    """

    defaults = {
        "logged_in": False,
        "username": None,
        "role": None,
        "agency_code": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
