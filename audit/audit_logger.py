from datetime import datetime
from audit.audit_schema import build_audit_record

AUDIT_LOG = []

def log_decision(**kwargs):
    record = build_audit_record(
        timestamp=datetime.utcnow(),
        **kwargs
    )
    AUDIT_LOG.append(record)
