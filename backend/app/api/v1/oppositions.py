import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.opposition_repo import OppositionRepository
from app.repositories.trademark_repo import TrademarkRepository
from app.schemas.opposition import (
    OppositionCaseCreate,
    OppositionCaseResponse,
    OppositionCaseUpdate,
    OppositionListResponse,
)

router = APIRouter()


@router.get("/trademarks/{trademark_id}/oppositions", response_model=OppositionListResponse)
async def list_oppositions(
    trademark_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    if not await TrademarkRepository(db).get_by_id(trademark_id):
        raise HTTPException(status_code=404, detail="Trademark not found")
    items = await OppositionRepository(db).list_by_trademark(trademark_id)
    return OppositionListResponse(items=items, total=len(items))


@router.post(
    "/trademarks/{trademark_id}/oppositions",
    response_model=OppositionCaseResponse,
    status_code=201,
)
async def create_opposition(
    trademark_id: uuid.UUID,
    data: OppositionCaseCreate,
    db: AsyncSession = Depends(get_db),
):
    if not await TrademarkRepository(db).get_by_id(trademark_id):
        raise HTTPException(status_code=404, detail="Trademark not found")
    return await OppositionRepository(db).create_for_trademark(trademark_id, data)


@router.get("/oppositions/{case_id}", response_model=OppositionCaseResponse)
async def get_opposition(case_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    case = await OppositionRepository(db).get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Opposition case not found")
    return case


@router.put("/oppositions/{case_id}", response_model=OppositionCaseResponse)
async def update_opposition(
    case_id: uuid.UUID,
    data: OppositionCaseUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = OppositionRepository(db)
    case = await repo.get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Opposition case not found")
    return await repo.update(case, data)


@router.delete("/oppositions/{case_id}", status_code=204)
async def delete_opposition(case_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = OppositionRepository(db)
    case = await repo.get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Opposition case not found")
    await repo.delete(case)
