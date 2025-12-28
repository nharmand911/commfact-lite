def build_audit_record(
    *,
    content_id,
    actor_role,
    decision,
    reason,
    severity,
    rule_ids,
    timestamp
):
    return {
        "content_id": content_id,
        "actor_role": actor_role,
        "decision": decision,
        "reason": reason,
        "severity": severity,
        "rule_ids": rule_ids,
        "timestamp": timestamp
    }
