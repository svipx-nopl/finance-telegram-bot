from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def unknown_message(message: Message):
    await message.answer(
        "Используйте кнопки меню."
    )