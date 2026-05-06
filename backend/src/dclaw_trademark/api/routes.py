from fastapi import APIRouter
from datetime import datetime
from uuid import uuid4
from dclaw_trademark.models import TrademarkCheck, TrademarkCreate

router = APIRouter()

@router.post("/checks", response_model=TrademarkCheck)
async def create_item(payload: TrademarkCreate):
    return TrademarkCheck(
        id=str(uuid4()),
        trademark_name=payload.trademark_name,
        trademark_class=payload.trademark_class,
        availability_status="likely_available",
        similar_marks=["AcmeMark", "Acmee", "ACME Solutions"],
        registration_likelihood="High - 85%",
        created_at=datetime.utcnow(),
    )

@router.get("/checks/{check_id}/watchlist")
async def get_item(check_id: str):
    return [{"mark": "NovaSync Pro", "status": "Registered"}, {"mark": "Nova-Sync", "status": "Pending"}, {"mark": "Novasync", "status": "Abandoned"}]
