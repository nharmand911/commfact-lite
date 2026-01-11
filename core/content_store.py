import streamlit as st
import uuid
from datetime import datetime
import hashlib

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
    Add new content to the in-memory queue with audit record.

    Features:
    - Generates unique content_id
    - Timestamp created_at
    - Creates record_hash (SHA256) for audit
    - Saves agency_code if provided
    """
    _init_content_queue()

    # Generate content_id & timestamp
    content_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    # 🔒 Generate record_hash (fingerprint unik)
    hash_input = f"{content_id}|{created_at}|{content_text}".encode("utf-8")
    record_hash = hashlib.sha256(hash_input).hexdigest()

    record = {
        "content_id": str(uuid.uuid4()),
        "content": content_text,
        "validation_result": validation_result,
        "created_by": created_by,
        "agency_code": agency_code,        # ✅ simpan agency_code
        "status": "SUBMITTED",
        "created_at": datetime.utcnow().isoformat(),
        "decision": validation_result.get("decision"),  # ambil dari hasil validasi
        "record_hash": record_hash
    }

    st.session_state[_CONTENT_QUEUE_KEY].append(record)
    return record
