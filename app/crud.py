from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from app import models, schemas


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        telegram_id=user.telegram_id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()
