import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.watchlist import WatchlistEntry
from app.repositories.base_repo import BaseRepository
from app.schemas.watchlist import WatchlistEntryCreate, WatchlistEntryUpdate


class WatchlistRepository(BaseRepository[WatchlistEntry]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, WatchlistEntry)

    async def list_by_trademark(self, trademark_id: uuid.UUID) -> List[WatchlistEntry]:
        result = await self.db.execute(
            select(WatchlistEntry).where(WatchlistEntry.trademark_id == trademark_id)
        )
        return list(result.scalars().all())

    async def create_for_trademark(
        self, trademark_id: uuid.UUID, data: WatchlistEntryCreate
    ) -> WatchlistEntry:
        entry = WatchlistEntry(trademark_id=trademark_id, **data.model_dump())
        return await self.create(entry)

    async def update(self, entry: WatchlistEntry, data: WatchlistEntryUpdate) -> WatchlistEntry:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry
