from governance.access_control import require_role

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

    content.status = decision
    return content.status
