from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from repositories.user_repository import UserRepository

router = Router()


@router.message(Command("register"))
async def register_handler(message: Message):

    user = await UserRepository.get_user_by_telegram_id(
        message.from_user.id
    )

    if user:

        await message.answer(
            "✅ Вы уже зарегистрированы"
        )

        return

    await UserRepository.create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.answer(
        "✅ Регистрация успешна"
    )


@router.message(Command("login"))
async def login_handler(message: Message):

    await message.answer(
        "✅ Авторизация выполнена"
    )

@router.message(Command("logout"))
async def logout_handler(message: Message):

    user = await UserRepository.get_user_by_telegram_id(
        message.from_user.id
    )

    if not user:

        await message.answer(
            "❌ Вы не зарегистрированы."
        )

        return

    await UserRepository.delete_user(
        message.from_user.id
    )

    await message.answer(
        "✅ Вы вышли из аккаунта.\n"
        "Теперь нужно зарегистрироваться заново:\n"
        "/register"
    )

@router.message(F.text == "🚪 Выйти")
async def logout_button_handler(message: Message):

    deleted = await UserRepository.delete_user(
        message.from_user.id
    )

    if not deleted:

        await message.answer(
            "❌ Вы не зарегистрированы."
        )

        return

    await message.answer(
        "✅ Вы вышли из аккаунта.\n\n"
        "Для повторной регистрации:\n"
        "/register"
    )

