import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from handlers.user_handlers import register_user_handlers
from handlers.admin_handler import admin_router

API_TOKEN = "5479451736:AAEdA5vB2dtxTWa9psPlv767Ingcpw_FA9U"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

from database import init_db

init_db()

async def main():
    register_user_handlers(dp)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
