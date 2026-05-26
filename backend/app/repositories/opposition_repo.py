import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.opposition import OppositionCase
from app.repositories.base_repo import BaseRepository
from app.schemas.opposition import OppositionCaseCreate, OppositionCaseUpdate


class OppositionRepository(BaseRepository[OppositionCase]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, OppositionCase)

    async def list_by_trademark(self, trademark_id: uuid.UUID) -> List[OppositionCase]:
        result = await self.db.execute(
            select(OppositionCase)
            .where(OppositionCase.trademark_id == trademark_id)
            .order_by(OppositionCase.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_for_trademark(
        self, trademark_id: uuid.UUID, data: OppositionCaseCreate
    ) -> OppositionCase:
        case = OppositionCase(trademark_id=trademark_id, **data.model_dump())
        return await self.create(case)

    async def update(
        self, case: OppositionCase, data: OppositionCaseUpdate
    ) -> OppositionCase:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(case, field, value)
        await self.db.commit()
        await self.db.refresh(case)
        return case
