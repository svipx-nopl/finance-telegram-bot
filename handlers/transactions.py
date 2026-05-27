from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

router = Router()


@router.message(Command("add_income"))
async def add_income_handler(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование: /add_income сумма категория"
        )
        return

    amount = args[1]
    category = args[2] if len(args) > 2 else "Другое"

    await message.answer(
        f"Доход добавлен: {amount} ₽ | {category}"
    )


@router.message(Command("add_expense"))
async def add_expense_handler(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование: /add_expense сумма категория"
        )
        return

    amount = args[1]
    category = args[2] if len(args) > 2 else "Другое"

    await message.answer(
        f"Расход добавлен: {amount} ₽ | {category}"
    )


@router.message(Command("view_transactions"))
async def view_transactions_handler(message: Message):
    await message.answer("История транзакций пока пуста")

@router.message(F.text == "➕ Доход")
async def income_button_handler(message: Message):
    await message.answer(
        "Введите доход:\n\nПример:\n/add_income 50000 зарплата"
    )


@router.message(F.text == "➖ Расход")
async def expense_button_handler(message: Message):
    await message.answer(
        "Введите расход:\n\nПример:\n/add_expense 2500 еда"
    )