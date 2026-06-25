from aiogram import BaseMiddleware
from aiogram.types import Message

from utils.auth import check_user_registered


class AuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler,
        event: Message,
        data
    ):

        if not event.text:
            return await handler(event, data)

        allowed_commands = [
            "/start",
            "/register",
            "/login",
            "/logout",
            "/cancel"
        ]

        if (
            event.text == "🚪 Выйти"
            or any(
                event.text.startswith(cmd)
                for cmd in allowed_commands
            )
        ):
            return await handler(event, data)

        is_registered = await check_user_registered(
            event
        )

        if not is_registered:
            return

        return await handler(event, data)

