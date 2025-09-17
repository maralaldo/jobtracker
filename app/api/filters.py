from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.crud import filters
from app.schemas.filter import FilterCreate, FilterRead, FilterUpdate

router = APIRouter(prefix="/filters", tags=["filters"])


@router.post("/", response_model=FilterRead)
async def create_filter(filter_in: FilterCreate, db: AsyncSession = Depends(get_session)):
    return await filters.create_filter(db=db, filter=filter_in)


@router.get("/{filter_id}", response_model=FilterRead)
async def read_filter(filter_id: int, db: AsyncSession = Depends(get_session)):
    db_filter = await filters.get_filter(db=db, filter_id=filter_id)
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")
    return db_filter


@router.get("/users/{user_id}/", response_model=list[FilterRead])
async def list_filters_by_user(user_id: int, db: AsyncSession = Depends(get_session)):
    return await filters.get_filters_by_user(db=db, user_id=user_id)


@router.patch("/{filter_id}", response_model=FilterRead)
async def update_filter(filter_id: int, filter_update: FilterUpdate, db: AsyncSession = Depends(get_session)):
    db_filter = await filters.update_filter(db, filter_id, filter_update)
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")
    return db_filter


@router.delete("/{filter_id}", status_code=204)
async def delete_filter(filter_id: int, db: AsyncSession = Depends(get_session)):
    ok = await filters.delete_filter(db, filter_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Filter not found")
    return Response(status_code=204)
