from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F


router = Router()


@router.message(Command("statistics"))
async def statistics_handler(message: Message):
    text = """
Статистика:

Доходы: 0 ₽
Расходы: 0 ₽
Баланс: 0 ₽
"""

    await message.answer(text)


@router.message(F.text == "📊 Статистика")
async def statistics_button_handler(message: Message):
    text = """
📊 Статистика:

Доходы: 0 ₽
Расходы: 0 ₽
Баланс: 0 ₽
"""

    await message.answer(text)