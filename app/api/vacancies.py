from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.crud import vacancy
from app.crud.vacancy import search_vacancies
from app.schemas.vacancy import VacancyCreate, VacancyRead, VacancyUpdate
from app.schemas.filter import VacancySearchRequest
from app.schemas.vacancy import VacancyOut

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.post("/", response_model=VacancyRead)
async def create_vacancy(vacancy_in: VacancyCreate, db: AsyncSession = Depends(get_session)):
    return await vacancy.create_vacancy(db=db, vacancy=vacancy_in)



@router.get("/", response_model=list[VacancyRead])
async def list_vacancies(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    return await vacancy.get_vacancies(db=db, skip=skip, limit=limit)


@router.get("/{vacancy_id}", response_model=VacancyRead)
async def read_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_session)):
    db_vacancy = await vacancy.get_vacancy(db=db, vacancy_id=vacancy_id)
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return db_vacancy


@router.patch("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy(vacancy_id: int, vacancy_update: VacancyUpdate, db: AsyncSession = Depends(get_session)):
    db_vacancy = await vacancy.update_vacancy(db, vacancy_id, vacancy_update)
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return db_vacancy


@router.delete("/{vacancy_id}", status_code=204)
async def delete_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_session)):
    ok = await vacancy.delete_vacancy(db, vacancy_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return Response(status_code=204)


@router.post("/search", response_model=List[VacancyOut])
async def search_vacancies_endpoint(
    search_request: VacancySearchRequest,
    db: AsyncSession = Depends(get_session)
):
    return await search_vacancies(
        db,
        filter_id=search_request.filter_id,
        keyword=search_request.keyword,
        location=search_request.location,
        min_salary=search_request.min_salary,
        max_salary=search_request.max_salary,
    )


@router.post("/parse")
async def trigger_parse(db: AsyncSession = Depends(get_session)):
    from app.tasks.vacancies import parse_vacancies
    parse_vacancies.delay()
    return {"status": "queued"}