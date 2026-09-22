import json
from datetime import datetime, timezone
from uuid import uuid4

from database.database import Database


class AuditLogger:

    def __init__(
        self,
        database: Database
    ):
        self.database = database

    def log(
        self,
        run_id: str,
        event_type: str,
        component: str,
        decision: str | None = None,
        reason: str | None = None,
        metadata: dict | None = None,
    ):

        event_id = str(uuid4())

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        self.database.insert_event(
            event_id=event_id,
            run_id=run_id,
            event_type=event_type,
            component=component,
            decision=decision,
            reason=reason,
            metadata=json.dumps(
                metadata or {}
            ),
            created_at=timestamp,
        )