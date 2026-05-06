from pydantic import BaseModel
from datetime import datetime
from typing import List

class TrademarkCheck(BaseModel):
    id: str
    trademark_name: str
    trademark_class: str
    availability_status: str
    similar_marks: list[str]
    registration_likelihood: str
    created_at: datetime

class TrademarkCreate(BaseModel):
    trademark_name: str
    trademark_class: str
