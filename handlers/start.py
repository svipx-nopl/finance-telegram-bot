from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.main_keyboard import main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    text = """
💰 Добро пожаловать в Finance Bot!

Этот бот помогает:
• учитывать доходы и расходы
• анализировать финансы
• отслеживать цели
• смотреть статистику и графики

📱 Используйте кнопки в меню ниже:

➕ Доход — добавить доход
➖ Расход — добавить расход
📄 Транзакции — история операций
📊 Статистика — аналитика и графики
🎯 Цели — финансовые цели и прогресс

⬇️ Меню находится под сообщением
"""

    await message.answer(
        text,
        reply_markup=main_keyboard
    )