import asyncio
from datetime import datetime, timedelta
from celery import shared_task
from aiogram import Bot
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.models.user import User
from app.models.vacancy import Vacancy


@shared_task
def send_notifications():
    """
    Celery task: sends new vacancies to users.
    """
    asyncio.run(_send_notifications())


async def _send_notifications():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id.isnot(None))
        )
        users = result.scalars().all()

        since = datetime.utcnow() - timedelta(days=1)
        result = await session.execute(
            select(Vacancy).where(Vacancy.created_at >= since)
        )
        vacancies = result.scalars().all()

        if not users or not vacancies:
            return

        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        for user in users:
            text = "📢 New vacancies:\n\n"
            for vac in vacancies:
                text += f"💼 {vac.title}\n🏢 {vac.company}\n📍 {vac.location}\n🔗 {vac.url}\n\n"

            try:
                await bot.send_message(user.telegram_id, text)
            except Exception as e:
                print(f"❌ Failed to send message to {user.telegram_id}: {e}")

        await bot.session.close()
