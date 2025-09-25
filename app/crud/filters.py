from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.models import Filter
from app.schemas.filter import FilterCreate, FilterUpdate


async def create_filter(db: AsyncSession, filter: FilterCreate):
    db_filter = Filter(**filter.model_dump())
    db.add(db_filter)
    await db.commit()
    await db.refresh(db_filter)
    return db_filter


async def get_all_filters(db: AsyncSession):
    result = await db.execute(select(models.Filter))
    return result.scalars().all()


async def get_filter(db: AsyncSession, filter_id: int):
    result = await db.execute(select(Filter).filter(Filter.id == filter_id))
    return result.scalars().first()


async def get_filters_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Filter).filter(Filter.user_id == user_id))
    return result.scalars().all()


async def update_filter(db: AsyncSession, filter_id: int, filter_in: FilterUpdate):
    result = await db.execute(select(Filter).filter(Filter.id == filter_id))
    db_filter = result.scalars().first()
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")

    for field, value in filter_in.model_dump(exclude_unset=True).items():
        setattr(db_filter, field, value)

    await db.commit()
    await db.refresh(db_filter)
    return db_filter


async def delete_filter(db: AsyncSession, filter_id: int):
    result = await db.execute(select(Filter).filter(Filter.id == filter_id))
    db_filter = result.scalars().first()
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")

    await db.delete(db_filter)
    await db.commit()
    return db_filter
