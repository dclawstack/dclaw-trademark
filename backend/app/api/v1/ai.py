from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.trademark_repo import TrademarkRepository
from app.services.application_drafter import draft_application
from app.services.class_recommender import suggest_classes
from app.services.copilot import chat

router = APIRouter()


class ClassSuggestionRequest(BaseModel):
    goods_services_description: str = Field(..., min_length=3, max_length=1000)


class CopilotRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    trademark_id: Optional[UUID] = None
    trademark_context: Optional[str] = None


@router.post("/suggest-classes")
async def suggest_nice_classes(payload: ClassSuggestionRequest):
    suggestions = await suggest_classes(payload.goods_services_description)
    return {"description": payload.goods_services_description, "suggestions": suggestions}


@router.post("/copilot/chat")
async def copilot_chat(payload: CopilotRequest, db: AsyncSession = Depends(get_db)):
    context = payload.trademark_context
    if payload.trademark_id and not context:
        repo = TrademarkRepository(db)
        tm = await repo.get_by_id(payload.trademark_id)
        if tm:
            context = (
                f"Trademark: {tm.name} | Owner: {tm.owner} | "
                f"Status: {tm.status} | Jurisdiction: {tm.jurisdiction}"
            )
    result = await chat(message=payload.message, trademark_context=context)
    return result


class DraftApplicationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    owner: str = Field(..., min_length=1, max_length=255)
    goods_services_description: str = Field(..., min_length=10, max_length=2000)


@router.post("/draft-application")
async def draft_trademark_application(payload: DraftApplicationRequest):
    result = await draft_application(
        name=payload.name,
        owner=payload.owner,
        goods_services_description=payload.goods_services_description,
    )
    return result


@router.post("/search/logo")
async def logo_similarity_search():
    return {
        "status": "not_implemented",
        "message": "Logo / visual similarity search is planned for v1.4. It requires object storage (MinIO) and a vision embedding model (CLIP). Coming soon.",
        "planned_version": "v1.4",
    }
