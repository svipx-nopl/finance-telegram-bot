from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("register"))
async def register_handler(message: Message):
    await message.answer("Регистрация успешна")


@router.message(Command("login"))
async def login_handler(message: Message):
    await message.answer("Авторизация выполнена")