import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trademark import Trademark, TrademarkClass
from app.repositories.base_repo import BaseRepository
from app.schemas.trademark import TrademarkCreate, TrademarkUpdate


class TrademarkRepository(BaseRepository[Trademark]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Trademark)

    async def create_with_classes(self, data: TrademarkCreate) -> Trademark:
        trademark = Trademark(
            name=data.name,
            owner=data.owner,
            status=data.status,
            jurisdiction=data.jurisdiction,
            application_number=data.application_number,
            registration_number=data.registration_number,
            filing_date=data.filing_date,
            registration_date=data.registration_date,
            expiry_date=data.expiry_date,
            description=data.description,
        )
        self.db.add(trademark)
        await self.db.flush()

        for cls in data.classes:
            self.db.add(
                TrademarkClass(
                    trademark_id=trademark.id,
                    nice_class_number=cls.nice_class_number,
                    description=cls.description,
                )
            )

        await self.db.commit()
        await self.db.refresh(trademark)
        return trademark

    async def update(self, trademark: Trademark, data: TrademarkUpdate) -> Trademark:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(trademark, field, value)
        await self.db.commit()
        await self.db.refresh(trademark)
        return trademark

    async def get_by_name(self, name: str) -> Optional[Trademark]:
        result = await self.db.execute(
            select(Trademark).where(Trademark.name.ilike(f"%{name}%"))
        )
        return result.scalars().first()
