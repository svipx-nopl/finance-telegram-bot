from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from repositories.transaction_repository import TransactionRepository

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

    category = (
        args[2]
        if len(args) > 2
        else "Другое"
    )

    await TransactionRepository.add_transaction(
        user_id=message.from_user.id,
        transaction_type="income",
        amount=float(amount),
        category=category
    )

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

    category = (
        args[2]
        if len(args) > 2
        else "Другое"
    )

    await TransactionRepository.add_transaction(
        user_id=message.from_user.id,
        transaction_type="expense",
        amount=float(amount),
        category=category
    )

    await message.answer(
        f"Расход добавлен: {amount} ₽ | {category}"
    )


@router.message(Command("view_transactions"))
async def view_transactions_handler(message: Message):

    transactions = await TransactionRepository.get_transactions(
        message.from_user.id
    )

    if not transactions:
        await message.answer(
            "У вас пока нет транзакций"
        )
        return

    text = "📄 История транзакций:\n\n"

    for transaction in transactions:

        transaction_type, amount, category, created_at = transaction

        emoji = "💰" if transaction_type == "income" else "💸"

        transaction_name = (
            "Доход"
            if transaction_type == "income"
            else "Расход"
        )

        text += (
            f"{emoji} {transaction_name}\n"
            f"💵 Сумма: {amount} ₽\n"
            f"📂 Категория: {category}\n"
            f"📅 Дата: {created_at}\n\n"
        )

    await message.answer(text)


@router.message(F.text == "➕ Доход")
async def income_button_handler(message: Message):

    await message.answer(
        "Введите доход:\n\n"
        "Пример:\n"
        "/add_income 50000 зарплата"
    )


@router.message(F.text == "➖ Расход")
async def expense_button_handler(message: Message):

    await message.answer(
        "Введите расход:\n\n"
        "Пример:\n"
        "/add_expense 2500 еда"
    )


@router.message(F.text == "📄 Транзакции")
async def transactions_button_handler(message: Message):

    transactions = await TransactionRepository.get_transactions(
        message.from_user.id
    )

    if not transactions:
        await message.answer(
            "У вас пока нет транзакций"
        )
        return

    text = "📄 История транзакций:\n\n"

    for transaction in transactions:

        transaction_type, amount, category, created_at = transaction

        emoji = "💰" if transaction_type == "income" else "💸"

        transaction_name = (
            "Доход"
            if transaction_type == "income"
            else "Расход"
        )

        text += (
            f"{emoji} {transaction_name}\n"
            f"💵 Сумма: {amount} ₽\n"
            f"📂 Категория: {category}\n"
            f"📅 Дата: {created_at}\n\n"
        )

    await message.answer(text)