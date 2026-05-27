from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message):
    text = """
Доступные команды:

/start - запуск бота
/help - помощь
/register - регистрация
/add_income - добавить доход
/add_expense - добавить расход
/view_transactions - история транзакций
/statistics - статистика
/set_goal - финансовая цель
"""

    await message.answer(text)