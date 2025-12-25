from governance.access_control import require_role
from audit.audit_logger import log_decision

def submit_decision(
    *,
    content,
    validation_result,
    decision: str,
    reason: str,
    user_role: str
):
    require_role(user_role, ["reviewer"])

    if not reason or reason.strip() == "":
        raise ValueError("Decision reason is mandatory")

    if decision == "APPROVED" and validation_result["final_severity"] == "HIGH":
        raise ValueError("High severity content cannot be approved")

    # update status
    content.status = decision

    # 🔒 audit log MUST be inside function
    log_decision(
        content_id=content.content_id,
        actor_role=user_role,
        decision=decision,
        reason=reason,
        severity=validation_result["final_severity"],
        rule_ids=[r["rule_id"] for r in validation_result["triggered_rules"]]
    )

    return content.status
