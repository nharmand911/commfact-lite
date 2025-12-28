import streamlit as st
from datetime import datetime
from typing import List, Dict, Any

_AUDIT_KEY = "AUDIT_LOG"


# =========================
# INTERNAL INIT
# =========================
def _init_audit_log() -> None:
    """
    Initialise audit log container in session_state.
    """
    if _AUDIT_KEY not in st.session_state:
        st.session_state[_AUDIT_KEY] = []


# =========================
# PUBLIC API
# =========================
def log_decision(
    *,
    content_id: str,
    content_excerpt: str,
    decision: str,
    reason: str,
    severity: str,
    rule_ids: List[str],
    actor: str,
    actor_role: str,
    agency_code: str | None,
    status_after: str
) -> None:
    """
    Append a decision record to the audit log.

    Append-only, session-bound (Streamlit).
    """
    _init_audit_log()

    record: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "content_id": content_id,
        "content_excerpt": content_excerpt[:200],
        "decision": decision,
        "reason": reason,
        "severity": severity,
        "rule_ids": list(rule_ids),
        "actor": actor,
        "actor_role": actor_role,
        "agency_code": agency_code,
        "status_after": status_after,
    }

    st.session_state[_AUDIT_KEY].append(record)


def get_audit_log() -> List[Dict[str, Any]]:
    """
    Return audit log (read-only copy).
    """
    _init_audit_log()
    return list(st.session_state[_AUDIT_KEY])
