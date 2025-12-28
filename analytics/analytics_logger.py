import streamlit as st
from datetime import datetime
import uuid

_ANALYTICS_KEY = "ANALYTICS_EVENTS"
APP_VERSION = "v0.1-pilot"


def _init_analytics():
    if _ANALYTICS_KEY not in st.session_state:
        st.session_state[_ANALYTICS_KEY] = []

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())


def log_event(
    *,
    event: str,
    object_type: str,
    object_id: str | None = None,
    username: str | None = None,
    role: str | None = None,
    agency_code: str | None = None
):
    """
    Pilot analytics logger (session-based, append-only)
    """

    _init_analytics()

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username or st.session_state.get("username"),
        "role": role or st.session_state.get("role"),
        "agency_code": agency_code or st.session_state.get("agency_code"),
        "event": event,
        "object_type": object_type,
        "object_id": object_id,
        "app_version": APP_VERSION,
        "session_id": st.session_state.get("session_id"),
    }

    st.session_state[_ANALYTICS_KEY].append(record)


def get_analytics_events():
    _init_analytics()
    return st.session_state[_ANALYTICS_KEY]
