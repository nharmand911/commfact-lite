import streamlit as st
import uuid
from datetime import datetime

_CONTENT_QUEUE_KEY = "CONTENT_QUEUE"


def _init_content_queue():
    if _CONTENT_QUEUE_KEY not in st.session_state:
        st.session_state[_CONTENT_QUEUE_KEY] = []


def get_content_queue():
    _init_content_queue()
    return st.session_state[_CONTENT_QUEUE_KEY]


def add_content_to_queue(
    *,
    content_text: str,
    validation_result: dict,
    created_by: str,
    agency_code: str | None = None  # ✅ tambahkan agency_code
):
    """
    Add new content to the in-memory queue.
    """
    _init_content_queue()

    record = {
        "content_id": str(uuid.uuid4()),
        "content": content_text,
        "validation_result": validation_result,
        "created_by": created_by,
        "agency_code": agency_code,        # ✅ simpan agency_code
        "status": "SUBMITTED",
        "created_at": datetime.utcnow().isoformat(),
        "decision": None
    }

    st.session_state[_CONTENT_QUEUE_KEY].append(record)
    return record
