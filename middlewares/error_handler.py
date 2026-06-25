import logging
from aiogram import BaseMiddleware

class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)

        except Exception:
            logging.exception("BOT CRASH INSIDE UPDATE")

            try:
                await event.answer("❌ Ошибка в боте")
            except:
                pass