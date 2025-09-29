import asyncio
from sqlalchemy.future import select
from app.core.database import get_session
from app.models.user import User


async def check_user(user_id: int):
    async for session in get_session():
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user:
            print(f"User {user.id}: {user.email}, telegram_id={user.telegram_id}")
        else:
            print(f"User with id={user_id} not found")


if __name__ == "__main__":
    asyncio.run(check_user(1))
