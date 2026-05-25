import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class WatchlistEntryBase(BaseModel):
    conflicting_mark_name: str
    similarity_score: Optional[float] = None
    conflict_type: str = "Phonetic"
    status: str = "Active"
    notes: Optional[str] = None


class WatchlistEntryCreate(WatchlistEntryBase):
    pass


class WatchlistEntryUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    similarity_score: Optional[float] = None


class WatchlistEntryResponse(WatchlistEntryBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    trademark_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class WatchlistListResponse(BaseModel):
    items: List[WatchlistEntryResponse]
    total: int
