import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.trademark_repo import TrademarkRepository
from app.schemas.trademark import (
    TrademarkCreate,
    TrademarkListResponse,
    TrademarkResponse,
    TrademarkUpdate,
)

router = APIRouter()


@router.get("/", response_model=TrademarkListResponse)
async def list_trademarks(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = TrademarkRepository(db)
    items, total = await repo.list_all(limit=limit, offset=offset)
    return TrademarkListResponse(items=items, total=total, limit=limit, offset=offset)


@router.post("/", response_model=TrademarkResponse, status_code=201)
async def create_trademark(
    data: TrademarkCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = TrademarkRepository(db)
    return await repo.create_with_classes(data)


@router.get("/{trademark_id}", response_model=TrademarkResponse)
async def get_trademark(
    trademark_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = TrademarkRepository(db)
    tm = await repo.get_by_id(trademark_id)
    if not tm:
        raise HTTPException(status_code=404, detail="Trademark not found")
    return tm


@router.put("/{trademark_id}", response_model=TrademarkResponse)
async def update_trademark(
    trademark_id: uuid.UUID,
    data: TrademarkUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = TrademarkRepository(db)
    tm = await repo.get_by_id(trademark_id)
    if not tm:
        raise HTTPException(status_code=404, detail="Trademark not found")
    return await repo.update(tm, data)


@router.delete("/{trademark_id}", status_code=204)
async def delete_trademark(
    trademark_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = TrademarkRepository(db)
    tm = await repo.get_by_id(trademark_id)
    if not tm:
        raise HTTPException(status_code=404, detail="Trademark not found")
    await repo.delete(tm)
