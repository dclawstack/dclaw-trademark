import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


VALID_STATUSES = {"Pending", "Registered", "Refused", "Abandoned", "Expired", "Cancelled"}
VALID_JURISDICTIONS = {"US", "EU", "WO", "UK", "CA", "AU", "CN", "JP", "IN", "BR"}


class TrademarkClassBase(BaseModel):
    nice_class_number: int
    description: Optional[str] = None


class TrademarkClassCreate(TrademarkClassBase):
    pass


class TrademarkClassResponse(TrademarkClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    trademark_id: uuid.UUID
    created_at: datetime


class TrademarkBase(BaseModel):
    name: str
    owner: str
    status: str = "Pending"
    jurisdiction: str = "US"
    application_number: Optional[str] = None
    registration_number: Optional[str] = None
    filing_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    description: Optional[str] = None


class TrademarkCreate(TrademarkBase):
    classes: List[TrademarkClassCreate] = []


class TrademarkUpdate(BaseModel):
    name: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    jurisdiction: Optional[str] = None
    application_number: Optional[str] = None
    registration_number: Optional[str] = None
    filing_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    description: Optional[str] = None


class TrademarkResponse(TrademarkBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    classes: List[TrademarkClassResponse] = []


class TrademarkListResponse(BaseModel):
    items: List[TrademarkResponse]
    total: int
    limit: int
    offset: int
