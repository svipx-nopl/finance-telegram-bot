from aiogram import BaseMiddleware
from aiogram.types import Message
from repositories.user_repository import UserRepository

class AuthMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data):

        commands_without_auth = [
            "/start",
            "/register",
            "/help"
        ]