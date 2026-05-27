from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.clearance_search import run_clearance_search

router = APIRouter()


class SearchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    classes: Optional[list[int]] = None
    jurisdiction: Optional[str] = None
    min_score: float = Field(default=0.2, ge=0.0, le=1.0)


@router.post("")
async def clearance_search(
    payload: SearchRequest,
    db: AsyncSession = Depends(get_db),
):
    results = await run_clearance_search(
        name=payload.name,
        classes=payload.classes,
        jurisdiction=payload.jurisdiction,
        min_score=payload.min_score,
        db=db,
    )
    return {"query": payload.name, "total": len(results), "results": results}
