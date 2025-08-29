from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import crud, schemas


router = APIRouter()


# Users
@router.post("/users/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    return await crud.get_user(db=db, user_id=user_id)


@router.patch("/users/{user_id}", response_model=schemas.UserRead)
async def update_user(user_id: int, user_update: schemas.UserUpdate, db: AsyncSession = Depends(get_session)):
    user = await crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)


# Vacancies
@router.post("/vacancies/", response_model=schemas.VacancyRead)
async def create_vacancy(vacancy: schemas.VacancyCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_vacancy(db=db, vacancy=vacancy)


@router.get("/vacancies/{vacancy_id}", response_model=schemas.VacancyRead)
async def read_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_session)):
    return await crud.get_vacancy(db=db, vacancy_id=vacancy_id)


# Filters
@router.post("/filters/", response_model=schemas.FilterRead)
async def create_filter(filter_data: schemas.FilterCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_filter(db=db, filter_data=filter_data)


@router.get("/filters/{filter_id}", response_model=schemas.FilterRead)
async def read_filter(filter_id: int, db: AsyncSession = Depends(get_session)):
    return await crud.get_filter(db=db, filter_id=filter_id)


@router.patch("/filters/{filter_id}", response_model=schemas.FilterRead)
async def update_filter(filter_id: int, filter_update: schemas.FilterUpdate, db: AsyncSession = Depends(get_session)):
    filter_obj = await crud.update_filter(db, filter_id, filter_update)
    if not filter_obj:
        raise HTTPException(status_code=404, detail="Filter not found")
    return filter_obj


@router.delete("/filters/{filter_id}", status_code=204)
async def delete_filter(filter_id: int, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_filter(db, filter_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Filter not found")
    return Response(status_code=204)
