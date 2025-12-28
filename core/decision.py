from datetime import datetime
from governance.access_control import require_role
from audit.audit_logger import write_audit_log


def submit_decision(
    *,
    content: dict,
    validation_result: dict,
    decision: str,
    reason: str,
    actor_username: str,
    actor_role: str,
    agency_code: str,
):
    """
    Submit reviewer decision for a content item.
    Content is a dict from content_store (NOT an ORM object).
    Records the decision to audit log (append-only).
    """

    # =========================
    # ACCESS CONTROL
    # =========================
    require_role(actor_role.lower(), ["reviewer"])

    # =========================
    # VALIDATION
    # =========================
    if not reason or not reason.strip():
        raise ValueError("Decision reason is mandatory")

    final_severity = validation_result.get("final_severity")

    if decision == "APPROVED" and final_severity == "HIGH":
        raise ValueError("High severity content cannot be approved")

    # =========================
    # UPDATE CONTENT STATE
    # =========================
    content["status"] = "DECIDED"
    content["decision"] = decision
    content["decided_at"] = datetime.utcnow().isoformat()

    # =========================
    # AUDIT LOG (APPEND-ONLY)
    # =========================
    write_audit_log({
        "timestamp": datetime.utcnow().isoformat(),
        "content_id": content.get("content_id"),
        "content_excerpt": content.get("content", "")[:200],
        "decision": decision,
        "reason": reason,
        "severity": final_severity,
        "triggered_rules": [
            r.get("rule_id") for r in validation_result.get("triggered_rules", [])
        ],
        "actor": actor_username,
        "actor_role": actor_role.lower(),
        "agency_code": agency_code,
        "status_after": "DECIDED",
    })

    return decision
