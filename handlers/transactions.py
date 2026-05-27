from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.transaction_states import AddTransactionState

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
async def income_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        AddTransactionState.waiting_for_amount
    )

    await state.update_data(
        transaction_type="income"
    )

    await message.answer(
        "💰 Введите сумму дохода:"
    )


@router.message(F.text == "➖ Расход")
async def expense_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        AddTransactionState.waiting_for_amount
    )

    await state.update_data(
        transaction_type="expense"
    )

    await message.answer(
        "💸 Введите сумму расхода:"
    )


@router.message(AddTransactionState.waiting_for_amount)
async def process_amount(
    message: Message,
    state: FSMContext
):

    try:

        amount = float(message.text)

    except ValueError:

        await message.answer(
            "Введите корректную сумму"
        )

        return

    await state.update_data(
        amount=amount
    )

    await state.set_state(
        AddTransactionState.waiting_for_category
    )

    await message.answer(
        "📂 Введите категорию:"
    )


@router.message(AddTransactionState.waiting_for_category)
async def process_category(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    transaction_type = data["transaction_type"]

    amount = data["amount"]

    category = message.text

    await TransactionRepository.add_transaction(
        user_id=message.from_user.id,
        transaction_type=transaction_type,
        amount=amount,
        category=category
    )

    transaction_name = (
        "Расход"
        if transaction_type == "expense"
        else "Доход"
    )

    await message.answer(
        f"✅ {transaction_name} добавлен\n\n"
        f"💵 Сумма: {amount} ₽\n"
        f"📂 Категория: {category}"
    )

    await state.clear()


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