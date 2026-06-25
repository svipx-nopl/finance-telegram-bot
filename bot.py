import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

from database.db import create_tables

from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.auth import router as auth_router
from handlers.transactions import router as transactions_router
from handlers.goals import router as goals_router
from handlers.statistics import router as statistics_router
from handlers.unknown import router as unknown_router

from middlewares.error_handler import ErrorMiddleware
from middlewares.auth_middleware import AuthMiddleware


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# middlewares
dp.message.middleware(AuthMiddleware())
dp.update.middleware(ErrorMiddleware())

# routers
dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(auth_router)
dp.include_router(transactions_router)
dp.include_router(goals_router)
dp.include_router(statistics_router)
dp.include_router(unknown_router)


async def main():
    await create_tables()

    print("🔥 BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())