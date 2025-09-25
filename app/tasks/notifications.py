import httpx
from app.core.config import settings


async def send_message_async(chat_id: str | int, text: str):
    if not getattr(settings, "TELEGRAM_BOT_TOKEN", None):
        return
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})
