from fastapi import APIRouter, HTTPException, Query

from app.services.nice_classes import get_all_classes, get_class, search_classes_by_keyword

router = APIRouter()


@router.get("")
async def list_classes(keyword: str = Query(default="", description="Filter by keyword")):
    if keyword:
        return search_classes_by_keyword(keyword)
    return get_all_classes()


@router.get("/{class_number}")
async def get_nice_class(class_number: int):
    result = get_class(class_number)
    if not result:
        raise HTTPException(status_code=404, detail=f"Nice class {class_number} not found")
    return result
