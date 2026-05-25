import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.trademark_repo import TrademarkRepository
from app.repositories.watchlist_repo import WatchlistRepository
from app.schemas.watchlist import (
    WatchlistEntryCreate,
    WatchlistEntryResponse,
    WatchlistEntryUpdate,
    WatchlistListResponse,
)

router = APIRouter()


@router.get("/trademarks/{trademark_id}/watchlist", response_model=WatchlistListResponse)
async def list_watchlist(
    trademark_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    tm_repo = TrademarkRepository(db)
    if not await tm_repo.get_by_id(trademark_id):
        raise HTTPException(status_code=404, detail="Trademark not found")
    repo = WatchlistRepository(db)
    items = await repo.list_by_trademark(trademark_id)
    return WatchlistListResponse(items=items, total=len(items))


@router.post(
    "/trademarks/{trademark_id}/watchlist",
    response_model=WatchlistEntryResponse,
    status_code=201,
)
async def add_watchlist_entry(
    trademark_id: uuid.UUID,
    data: WatchlistEntryCreate,
    db: AsyncSession = Depends(get_db),
):
    tm_repo = TrademarkRepository(db)
    if not await tm_repo.get_by_id(trademark_id):
        raise HTTPException(status_code=404, detail="Trademark not found")
    repo = WatchlistRepository(db)
    return await repo.create_for_trademark(trademark_id, data)


@router.put("/watchlist/{entry_id}", response_model=WatchlistEntryResponse)
async def update_watchlist_entry(
    entry_id: uuid.UUID,
    data: WatchlistEntryUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = WatchlistRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Watchlist entry not found")
    return await repo.update(entry, data)


@router.delete("/watchlist/{entry_id}", status_code=204)
async def delete_watchlist_entry(
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    repo = WatchlistRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Watchlist entry not found")
    await repo.delete(entry)
