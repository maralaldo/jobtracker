from dotenv import load_dotenv
load_dotenv()
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
import asyncio
import os


from app.core.database import AsyncSessionLocal
from app.crud.users import link_telegram_id

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.update()
async def log_all_updates(update: Update):
    if update.message:
        user = update.message.from_user
        logging.info(
            f"📩 Message from {user.username or user.full_name} "
            f"(id={user.id}): {update.message.text!r}"
        )
    elif update.callback_query:
        user = update.callback_query.from_user
        logging.info(
            f"🔘 Callback from {user.username or user.full_name} "
            f"(id={user.id}): {update.callback_query.data!r}"
        )
    else:
        logging.info(f"⚡ Other update: {update}")


@dp.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    logging.info(f"➡️ /start from id={telegram_id}")

    async with AsyncSessionLocal() as session:
        user = await link_telegram_id(session, user_id=1, telegram_id=str(telegram_id))

    if user:
        await message.answer("✅ Your Telegram ID has been linked to your account!")
    else:
        await message.answer("⚠️ User not found in database.")


async def main():
    logging.info("🤖 Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
