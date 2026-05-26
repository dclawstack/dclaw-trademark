from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.clearance_search import run_clearance_search

router = APIRouter()


class SearchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    classes: Optional[list[int]] = None
    jurisdiction: Optional[str] = None
    min_score: float = Field(default=0.2, ge=0.0, le=1.0)


@router.post("")
async def clearance_search(payload: SearchRequest):
    results = run_clearance_search(
        name=payload.name,
        classes=payload.classes,
        jurisdiction=payload.jurisdiction,
        min_score=payload.min_score,
    )
    return {"query": payload.name, "total": len(results), "results": results}
