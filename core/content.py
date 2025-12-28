import uuid
from datetime import datetime

class Content:
    def __init__(self, text: str, created_by: str):
        self.content_id = str(uuid.uuid4())
        self.text = text
        self.created_by = created_by
        self.status = "DRAFT"
        self.created_at = datetime.utcnow()
