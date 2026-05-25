import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


VALID_DEADLINE_TYPES = {
    "RENEWAL",
    "RESPONSE",
    "OPPOSITION",
    "STATEMENT_OF_USE",
    "MAINTENANCE",
    "OTHER",
}
VALID_STATUSES = {"Pending", "Completed", "Dismissed", "Overdue"}


class DeadlineAlertBase(BaseModel):
    deadline_type: str
    due_date: datetime
    status: str = "Pending"
    notes: Optional[str] = None


class DeadlineAlertCreate(DeadlineAlertBase):
    pass


class DeadlineAlertUpdate(BaseModel):
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None


class DeadlineAlertResponse(DeadlineAlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    trademark_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DeadlineListResponse(BaseModel):
    items: List[DeadlineAlertResponse]
    total: int
