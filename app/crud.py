from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from app import models, schemas


# User CRUD
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,  # TODO: hash password
        telegram_id=user.telegram_id,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_in: schemas.UserUpdate):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None

    data = user_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return False

    await db.delete(db_user)
    await db.commit()
    return True


# Vacancy CRUD
async def create_vacancy(db: AsyncSession, vacancy: schemas.VacancyCreate):
    db_vacancy = models.Vacancy(
        title=vacancy.title,
        company=vacancy.company,
        location=vacancy.location,
        salary=vacancy.salary,
        url=vacancy.url,
        source=vacancy.source,
    )
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy


async def get_vacancy(db: AsyncSession, vacancy_id: int):
    result = await db.execute(select(models.Vacancy).where(models.Vacancy.id == vacancy_id))
    return result.scalar_one_or_none()


async def get_vacancies(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Vacancy).offset(skip).limit(limit))
    return result.scalars().all()


# Filter CRUD
async def create_filter(db: AsyncSession, filter_data: schemas.FilterCreate):
    db_filter = models.Filter(
        user_id=filter_data.user_id,
        keyword=filter_data.keyword,
        location=filter_data.location,
        min_salary=filter_data.min_salary,
        max_salary=filter_data.max_salary,
    )
    db.add(db_filter)
    await db.commit()
    await db.refresh(db_filter)
    return db_filter


async def get_filters_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Filter).where(models.Filter.user_id == user_id))
    return result.scalars().all()


async def get_filter(db: AsyncSession, filter_id: int):
    result = await db.execute(select(models.Filter).where(models.Filter.id == filter_id))
    return result.scalar_one_or_none()
