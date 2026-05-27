from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.main_keyboard import main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    text = """
💰 Добро пожаловать в Finance Bot!

Этот бот поможет:
• учитывать доходы и расходы
• анализировать бюджет
• отслеживать финансовые цели

📌 Доступные команды:

/register — регистрация пользователя

/add_income [сумма] [категория]
➜ добавить доход

/add_expense [сумма] [категория]
➜ добавить расход

/view_transactions
➜ история транзакций

/set_goal [сумма] [описание]
➜ установить финансовую цель

/statistics
➜ статистика и аналитика

/help
➜ список всех команд
"""

    await message.answer(
        text,
        reply_markup=main_keyboard
    )