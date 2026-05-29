import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class ErrorMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data
    ):

        try:
            return await handler(event, data)

        except Exception as e:

            logging.exception(
                f"Ошибка: {e}"
            )

            if hasattr(event, "answer"):

                await event.answer(
                    "❌ Произошла ошибка.\n"
                    "Попробуйте позже."
                )