from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models import Vacancy
from app.schemas.vacancy import VacancyCreate, VacancyUpdate


async def create_vacancy(db: AsyncSession, vacancy: VacancyCreate):
    db_vacancy = Vacancy(**vacancy.model_dump())
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy


async def get_vacancies(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Vacancy).offset(skip).limit(limit))
    return result.scalars().all()


async def get_vacancy(db: AsyncSession, vacancy_id: int):
    result = await db.execute(select(Vacancy).filter(Vacancy.id == vacancy_id))
    return result.scalars().first()


async def update_vacancy(db: AsyncSession, vacancy_id: int, vacancy_in: VacancyUpdate):
    result = await db.execute(select(Vacancy).filter(Vacancy.id == vacancy_id))
    db_vacancy = result.scalars().first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    for field, value in vacancy_in.model_dump(exclude_unset=True).items():
        setattr(db_vacancy, field, value)

    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy


async def delete_vacancy(db: AsyncSession, vacancy_id: int):
    result = await db.execute(select(Vacancy).filter(Vacancy.id == vacancy_id))
    db_vacancy = result.scalars().first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    await db.delete(db_vacancy)
    await db.commit()
    return db_vacancy
