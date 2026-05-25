import uuid
from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deadline import DeadlineAlert
from app.repositories.base_repo import BaseRepository
from app.schemas.deadline import DeadlineAlertCreate, DeadlineAlertUpdate


class DeadlineRepository(BaseRepository[DeadlineAlert]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, DeadlineAlert)

    async def list_by_trademark(self, trademark_id: uuid.UUID) -> List[DeadlineAlert]:
        result = await self.db.execute(
            select(DeadlineAlert).where(DeadlineAlert.trademark_id == trademark_id)
        )
        return list(result.scalars().all())

    async def list_upcoming(self, cutoff: datetime) -> List[DeadlineAlert]:
        result = await self.db.execute(
            select(DeadlineAlert)
            .where(DeadlineAlert.due_date <= cutoff)
            .where(DeadlineAlert.status == "Pending")
            .order_by(DeadlineAlert.due_date)
        )
        return list(result.scalars().all())

    async def create_for_trademark(
        self, trademark_id: uuid.UUID, data: DeadlineAlertCreate
    ) -> DeadlineAlert:
        alert = DeadlineAlert(trademark_id=trademark_id, **data.model_dump())
        return await self.create(alert)

    async def update(self, alert: DeadlineAlert, data: DeadlineAlertUpdate) -> DeadlineAlert:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(alert, field, value)
        await self.db.commit()
        await self.db.refresh(alert)
        return alert
