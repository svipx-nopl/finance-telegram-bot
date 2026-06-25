from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.transaction_states import AddTransactionState
from utils.validators import validate_amount, validate_category
from utils.auth import get_current_user
from repositories.transaction_repository import TransactionRepository

router = Router()


@router.message(Command("add_income"))
async def add_income_handler(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /add_income сумма категория")
        return

    amount = args[1]

    is_valid, result = validate_amount(amount)
    if not is_valid:
        await message.answer(result)
        return

    category = args[2] if len(args) > 2 else "Другое"

    is_valid, result = validate_category(category, "income")
    if not is_valid:
        await message.answer(result)
        return

    user = await get_current_user(message)

    await TransactionRepository.add_transaction(
        user_id=user[0],
        transaction_type="income",
        amount=result,
        category=category
    )

    await message.answer(f"Доход добавлен: {result} ₽ | {category}")


@router.message(Command("add_expense"))
async def add_expense_handler(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /add_expense сумма категория")
        return

    amount = args[1]

    is_valid, result = validate_amount(amount)
    if not is_valid:
        await message.answer(result)
        return

    category = args[2] if len(args) > 2 else "Другое"

    is_valid, result = validate_category(category, "expense")
    if not is_valid:
        await message.answer(result)
        return

    user = await get_current_user(message)

    await TransactionRepository.add_transaction(
        user_id=user[0],
        transaction_type="expense",
        amount=result,
        category=category
    )

    await message.answer(f"Расход добавлен: {result} ₽ | {category}")


@router.message(Command("view_transactions"))
async def view_transactions_handler(message: Message):
    user = await get_current_user(message)

    transactions = await TransactionRepository.get_transactions(user[0])

    if not transactions:
        await message.answer("У вас пока нет транзакций")
        return

    text = "📄 История транзакций:\n\n"

    for t in transactions:
        tid, ttype, amount, category, created_at = t

        emoji = "💰" if ttype == "income" else "💸"
        name = "Доход" if ttype == "income" else "Расход"

        text += (
            f"{emoji} {name}\n"
            f"💵 Сумма: {amount} ₽\n"
            f"📂 Категория: {category}\n"
            f"📅 Дата: {created_at}\n\n"
        )

    await message.answer(text)


@router.message(F.text == "➕ Доход")
async def income_start(message: Message, state: FSMContext):
    current = await state.get_state()
    if current:
        await message.answer("❌ Завершите текущее действие /cancel")
        return

    await state.set_state(AddTransactionState.waiting_for_amount)
    await state.update_data(type="income")
    await message.answer("💰 Введите сумму дохода:")


@router.message(F.text == "➖ Расход")
async def expense_start(message: Message, state: FSMContext):
    current = await state.get_state()
    if current:
        await message.answer("❌ Завершите текущее действие /cancel")
        return

    await state.set_state(AddTransactionState.waiting_for_amount)
    await state.update_data(type="expense")
    await message.answer("💸 Введите сумму расхода:")


@router.message(AddTransactionState.waiting_for_amount, F.text.regexp(r"^\d+(\.\d+)?$"))
async def process_amount(message: Message, state: FSMContext):
    amount = float(message.text)

    await state.update_data(amount=amount)
    await state.set_state(AddTransactionState.waiting_for_category)

    await message.answer("📂 Введите категорию:")


@router.message(AddTransactionState.waiting_for_amount)
async def invalid_amount(message: Message):
    await message.answer("❌ Введите число")


@router.message(AddTransactionState.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    data = await state.get_data()

    user = await get_current_user(message)

    is_valid, category = validate_category(message.text, data["type"])
    if not is_valid:
        await message.answer(category)
        return

    await TransactionRepository.add_transaction(
        user_id=user[0],
        transaction_type=data["type"],
        amount=data["amount"],
        category=category
    )

    await state.clear()

    await message.answer(
        f"✅ Добавлено\n💵 {data['amount']} ₽\n📂 {category}"
    )


@router.message(F.text == "📄 Транзакции")
async def transactions_button(message: Message):
    user = await get_current_user(message)

    transactions = await TransactionRepository.get_transactions(user[0])

    if not transactions:
        await message.answer("У вас пока нет транзакций")
        return

    text = "📄 История транзакций:\n\n"

    for t in transactions:
        tid, ttype, amount, category, created_at = t

        emoji = "💰" if ttype == "income" else "💸"
        name = "Доход" if ttype == "income" else "Расход"

        text += f"{emoji} {name}\n💵 {amount} ₽\n📂 {category}\n📅 {created_at}\n\n"

    await message.answer(text)


@router.message(F.text == "🗑 Удалить транзакцию")
async def delete_start(message: Message, state: FSMContext):
    user = await get_current_user(message)

    transactions = await TransactionRepository.get_transactions(user[0])

    if not transactions:
        await message.answer("❌ Транзакций нет")
        return

    text = "📄 Ваши транзакции:\n\n"

    for t in transactions:
        text += f"ID: {t[0]} | {t[1]} | {t[3]} | {t[2]} ₽\n"

    await state.set_state(AddTransactionState.waiting_for_delete_id)

    await message.answer(text + "\nВведите ID:")


@router.message(AddTransactionState.waiting_for_delete_id)
async def delete_process(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ ID числом")
        return

    user = await get_current_user(message)

    deleted = await TransactionRepository.delete_transaction(int(message.text), user[0])

    if not deleted:
        await message.answer("❌ Не найдено")
        return

    await state.clear()
    await message.answer("✅ Удалено")


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Отменено")

@router.message(F.text == "test")
async def test(message: Message):
    print("TEST HIT")
    await message.answer("OK")