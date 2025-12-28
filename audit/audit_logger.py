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
    status_after: str,
    agency_code: str | None = None
) -> None:
    """
    Append a decision record to the audit log.

    This function is intentionally append-only
    to support tamper-evident audit trails.
    """
    _init_audit_log()

    record: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "content_id": content_id,
        "content_excerpt": content_excerpt[:200],  # 🔒 safety trim
        "decision": decision,
        "reason": reason,
        "severity": severity,
        "rule_ids": list(rule_ids),                # 🔒 defensive copy
        "actor": actor,                            # reviewer username
        "actor_role": actor_role,                  # Reviewer / Admin
        "agency_code": agency_code,                # 🏢 multi-agency
        "status_after": status_after
    }

    st.session_state[_AUDIT_KEY].append(record)


def get_audit_log() -> List[Dict[str, Any]]:
    """
    Return full audit log (read-only usage expected).
    """
    _init_audit_log()
    return list(st.session_state[_AUDIT_KEY])      # 🔒 defensive copy
