import os

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from health import health

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

dp.message.middleware(AuthMiddleware())
dp.update.middleware(ErrorMiddleware())

dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(auth_router)
dp.include_router(transactions_router)
dp.include_router(goals_router)
dp.include_router(statistics_router)
dp.include_router(unknown_router)


async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)


def main():
    app = web.Application()

    app.on_startup.append(lambda app: on_startup(bot))

    SimpleRequestHandler(dp, bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.router.add_get("/health", health)

    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))


if __name__ == "__main__":
    main()