import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OppositionCaseBase(BaseModel):
    case_type: str = "Opposition"
    stage: str = "Filed"
    case_number: Optional[str] = None
    opposing_party: Optional[str] = None
    opposing_counsel: Optional[str] = None
    filing_date: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    hearing_date: Optional[datetime] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None


class OppositionCaseCreate(OppositionCaseBase):
    pass


class OppositionCaseUpdate(BaseModel):
    case_type: Optional[str] = None
    stage: Optional[str] = None
    case_number: Optional[str] = None
    opposing_party: Optional[str] = None
    opposing_counsel: Optional[str] = None
    filing_date: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    hearing_date: Optional[datetime] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None


class OppositionCaseResponse(OppositionCaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    trademark_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class OppositionListResponse(BaseModel):
    items: list[OppositionCaseResponse]
    total: int
