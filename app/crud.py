from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app import models, schemas
from app.security import hash_password


# User CRUD
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()



async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        telegram_id=user.telegram_id,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_in: schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password":
            setattr(db_user, "hashed_password", hash_password(value))
        else:
            setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()
    return db_user



# Vacancy CRUD
async def create_vacancy(db: AsyncSession, vacancy: schemas.VacancyCreate):
    db_vacancy = models.Vacancy(**vacancy.model_dump())
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy


async def get_vacancies(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Vacancy).offset(skip).limit(limit))
    return result.scalars().all()


async def update_vacancy(db: AsyncSession, vacancy_id: int, vacancy_in: schemas.VacancyUpdate):
    result = await db.execute(select(models.Vacancy).filter(models.Vacancy.id == vacancy_id))
    db_vacancy = result.scalars().first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    for field, value in vacancy_in.model_dump(exclude_unset=True).items():
        setattr(db_vacancy, field, value)

    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy


async def delete_vacancy(db: AsyncSession, vacancy_id: int):
    result = await db.execute(select(models.Vacancy).filter(models.Vacancy.id == vacancy_id))
    db_vacancy = result.scalars().first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    await db.delete(db_vacancy)
    await db.commit()
    return db_vacancy



# Filter CRUD
async def create_filter(db: AsyncSession, filter: schemas.FilterCreate):
    db_filter = models.Filter(**filter.model_dump())
    db.add(db_filter)
    await db.commit()
    await db.refresh(db_filter)
    return db_filter


async def get_filters(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Filter).options(joinedload(models.Filter.user)).filter(models.Filter.user_id == user_id)
    )
    return result.scalars().all()


async def update_filter(db: AsyncSession, filter_id: int, filter_in: schemas.FilterUpdate):
    result = await db.execute(select(models.Filter).filter(models.Filter.id == filter_id))
    db_filter = result.scalars().first()
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")

    for field, value in filter_in.model_dump(exclude_unset=True).items():
        setattr(db_filter, field, value)

    await db.commit()
    await db.refresh(db_filter)
    return db_filter


async def delete_filter(db: AsyncSession, filter_id: int):
    result = await db.execute(select(models.Filter).filter(models.Filter.id == filter_id))
    db_filter = result.scalars().first()
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")

    await db.delete(db_filter)
    await db.commit()
    return db_filter