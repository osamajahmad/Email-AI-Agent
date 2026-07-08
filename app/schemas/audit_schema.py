from typing import Any, Dict

from pydantic import BaseModel, Field


class AuditLogSchema(BaseModel):
    """
    Structure of one audit log entry.

    Current audit logs are stored in memory during development.
    Later, this can be moved to a database.
    """

    timestamp: str
    user: str
    event_type: str
    details: Dict[str, Any] = Field(default_factory=dict)