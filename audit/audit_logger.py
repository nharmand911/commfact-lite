from datetime import datetime
from typing import List, Dict, Any

# ======================================
# GLOBAL APPEND-ONLY AUDIT STORE (MVP)
# ======================================
_AUDIT_LOG: List[Dict[str, Any]] = []


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
    agency_code: str | None = None,
) -> None:
    """
    Append a decision record to the audit log.

    Append-only, in-memory (MVP).
    """

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

    _AUDIT_LOG.append(record)


def get_audit_log() -> List[Dict[str, Any]]:
    """
    Return full audit log (read-only).
    """
    return list(_AUDIT_LOG)
