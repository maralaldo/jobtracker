from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.models import Vacancy
from app.models.filter import Filter
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


async def get_vacancy_by_url(db: AsyncSession, url: str):
    result = await db.execute(select(models.Vacancy).where(models.Vacancy.url == url))
    return result.scalar_one_or_none()


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


async def search_vacancies(
    db: AsyncSession,
    filter_id: Optional[int] = None,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None,
) -> List[Vacancy]:
    if filter_id:
        db_filter = await db.get(Filter, filter_id)
        if db_filter:
            keyword = keyword or db_filter.keyword
            location = location or db_filter.location
            min_salary = min_salary or db_filter.min_salary
            max_salary = max_salary or db_filter.max_salary

    query = select(Vacancy)

    if keyword:
        query = query.filter(
            (Vacancy.title.ilike(f"%{keyword}%")) |
            (Vacancy.company.ilike(f"%{keyword}%"))
        )
    if location:
        query = query.filter(Vacancy.location.ilike(f"%{location}%"))
    if min_salary:
        query = query.filter(Vacancy.salary >= min_salary)
    if max_salary:
        query = query.filter(Vacancy.salary <= max_salary)

    result = await db.execute(query)
    return result.scalars().all()