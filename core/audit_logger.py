import uuid
from datetime import datetime, timezone


class AuditLogger:

    def __init__(self, database):
        self.database = database

    def log(
        self,
        run_id,
        event_type,
        component,
        decision,
        reason,
        metadata=None,
    ):

        event = {
            "event_id": str(uuid.uuid4()),
            "run_id": run_id,
            "event_type": event_type,
            "component": component,
            "decision": decision,
            "reason": reason,
            "metadata": metadata or {},
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        self.database.insert_event(event)

        return event