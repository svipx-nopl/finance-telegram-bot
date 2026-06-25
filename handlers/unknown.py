from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def unknown(message: Message):
    await message.answer("❌ Используйте кнопки меню")

from aiogram import F

@router.message()
async def debug(message):
    print("DEBUG HIT:", message.text)
    await message.answer("OK")