import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.utils import utc_now
from app.repositories.deadline_repo import DeadlineRepository
from app.repositories.trademark_repo import TrademarkRepository
from app.schemas.deadline import (
    DeadlineAlertCreate,
    DeadlineAlertResponse,
    DeadlineAlertUpdate,
    DeadlineListResponse,
)

router = APIRouter()


@router.get("/trademarks/{trademark_id}/deadlines", response_model=DeadlineListResponse)
async def list_deadlines(
    trademark_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    tm_repo = TrademarkRepository(db)
    if not await tm_repo.get_by_id(trademark_id):
        raise HTTPException(status_code=404, detail="Trademark not found")
    repo = DeadlineRepository(db)
    items = await repo.list_by_trademark(trademark_id)
    return DeadlineListResponse(items=items, total=len(items))


@router.post(
    "/trademarks/{trademark_id}/deadlines",
    response_model=DeadlineAlertResponse,
    status_code=201,
)
async def create_deadline(
    trademark_id: uuid.UUID,
    data: DeadlineAlertCreate,
    db: AsyncSession = Depends(get_db),
):
    tm_repo = TrademarkRepository(db)
    if not await tm_repo.get_by_id(trademark_id):
        raise HTTPException(status_code=404, detail="Trademark not found")
    repo = DeadlineRepository(db)
    return await repo.create_for_trademark(trademark_id, data)


@router.get("/deadlines/upcoming", response_model=DeadlineListResponse)
async def upcoming_deadlines(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    cutoff = utc_now() + timedelta(days=days)
    repo = DeadlineRepository(db)
    items = await repo.list_upcoming(cutoff)
    return DeadlineListResponse(items=items, total=len(items))


@router.put("/deadlines/{deadline_id}", response_model=DeadlineAlertResponse)
async def update_deadline(
    deadline_id: uuid.UUID,
    data: DeadlineAlertUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = DeadlineRepository(db)
    alert = await repo.get_by_id(deadline_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Deadline not found")
    return await repo.update(alert, data)


@router.delete("/deadlines/{deadline_id}", status_code=204)
async def delete_deadline(
    deadline_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = DeadlineRepository(db)
    alert = await repo.get_by_id(deadline_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Deadline not found")
    await repo.delete(alert)
