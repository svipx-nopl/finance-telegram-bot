from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.transaction_states import AddTransactionState
from utils.validators import (
    validate_amount,
    validate_category
)
from utils.auth import (
    check_user_registered,
    get_current_user
)
from aiogram.filters import StateFilter




from repositories.transaction_repository import TransactionRepository

router = Router()


@router.message(Command("add_income"))
async def add_income_handler(message: Message):
    if not await check_user_registered(message):
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование: /add_income сумма категория"
        )
        return

    amount = args[1]

    is_valid, result = validate_amount(amount)

    if not is_valid:

        await message.answer(result)
        return

    amount = result

    category = (
        args[2]
        if len(args) > 2
        else "Другое"
    )

    is_valid, result = validate_category(
        category,
        "income"
    )

    if not is_valid:
        await message.answer(result)
        return

    category = result

    user = await get_current_user(message)

    await TransactionRepository.add_transaction(
        user_id=user[0],
        transaction_type="income",
        amount=amount,
        category=category
    )

    await message.answer(
        f"Доход добавлен: {amount} ₽ | {category}"
    )


@router.message(Command("add_expense"))
async def add_expense_handler(message: Message):
    if not await check_user_registered(message):
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование: /add_expense сумма категория"
        )
        return

    amount = args[1]

    is_valid, result = validate_amount(amount)

    if not is_valid:
        await message.answer(result)
        return

    amount = result

    category = (
        args[2]
        if len(args) > 2
        else "Другое"
    )

    is_valid, result = validate_category(
        category,
        "expense"
    )

    if not is_valid:
        await message.answer(result)
        return

    category = result

    user = await get_current_user(message)

    await TransactionRepository.add_transaction(
        user_id=user[0],
        transaction_type="expense",
        amount=amount,
        category=category
    )

    await message.answer(
        f"Расход добавлен: {amount} ₽ | {category}"
    )


@router.message(Command("view_transactions"))
async def view_transactions_handler(message: Message):
    if not await check_user_registered(message):
        return
    user = await get_current_user(message)

    transactions = await TransactionRepository.get_transactions(
        user[0]
    )

    if not transactions:
        await message.answer(
            "У вас пока нет транзакций"
        )
        return

    text = "📄 История транзакций:\n\n"

    for transaction in transactions:

        transaction_id, transaction_type, amount, category, created_at = transaction

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
    if not await check_user_registered(message):
        return

    current_state = await state.get_state()

    if current_state:
        await message.answer(
            "❌ Сначала завершите текущее действие или используйте /cancel"
        )
        return

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
    if not await check_user_registered(message):
        return

    current_state = await state.get_state()

    if current_state:
        await message.answer(
            "❌ Сначала завершите текущее действие или используйте /cancel"
        )
        return

    await state.set_state(
        AddTransactionState.waiting_for_amount
    )

    await state.update_data(
        transaction_type="expense"
    )

    await message.answer(
        "💸 Введите сумму расхода:"
    )


@router.message(
    AddTransactionState.waiting_for_amount,
    F.text.regexp(r"^\d+(\.\d+)?$")
)
async def process_amount(
message: Message,
state: FSMContext
):




    if not await check_user_registered(message):
        await state.clear()
        return

    is_valid, result = validate_amount(
        message.text
    )

    if not is_valid:

        await message.answer(result)
        return

    amount = result

    await state.update_data(
        amount=amount
    )

    await state.set_state(
        AddTransactionState.waiting_for_category
    )

    await message.answer(
        "📂 Введите категорию:"
    )


@router.message(
    AddTransactionState.waiting_for_amount,
    ~F.text.startswith("/")
)
async def invalid_amount(
    message: Message,
    state: FSMContext
):

    if not await check_user_registered(message):
        await state.clear()
        return

    await message.answer(
        "❌ Введите сумму числом."
    )


@router.message(
    AddTransactionState.waiting_for_category,
    ~F.text.startswith("/")
)
async def process_category(
    message: Message,
    state: FSMContext
):

    if not await check_user_registered(message):
        await state.clear()
        return

    data = await state.get_data()

    transaction_type = data["transaction_type"]
    amount = data["amount"]

    is_valid, result = validate_category(
        message.text,
        transaction_type
    )

    if not is_valid:

        await message.answer(result)
        return

    category = result

    user = await get_current_user(message)

    await TransactionRepository.add_transaction(
        user_id=user[0],
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

    if not await check_user_registered(message):
        return

    user = await get_current_user(message)

    transactions = await TransactionRepository.get_transactions(
        user[0]
    )

    if not transactions:
        await message.answer(
            "У вас пока нет транзакций"
        )
        return

    text = "📄 История транзакций:\n\n"

    for transaction in transactions:

        transaction_id, transaction_type, amount, category, created_at = transaction

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


@router.message(
    F.text == "🗑 Удалить транзакцию"
)
async def delete_transaction_start(
    message: Message,
    state: FSMContext
):
    if not await check_user_registered(message):
        return

    user = await get_current_user(message)

    transactions = await (
        TransactionRepository
        .get_transactions(
            user[0]
        )
    )



    if not transactions:

        await message.answer(
            "❌ Транзакций нет."
        )
        return

    text = "📄 Ваши транзакции:\n\n"

    for transaction in transactions:
        text += (
            f"ID: {transaction[0]} | "
            f"{transaction[1]} | "
            f"{transaction[3]} | "
            f"{transaction[2]} ₽\n"
        )

    await state.set_state(
        AddTransactionState
        .waiting_for_delete_id
    )

    await message.answer(
        text +
        "\nВведите ID транзакции "
        "для удаления:"
    )


@router.message(
    AddTransactionState.waiting_for_delete_id,
    ~F.text.startswith("/")
)
async def process_delete_transaction(
    message: Message,
    state: FSMContext
):
    if not await check_user_registered(message):
        await state.clear()
        return

    if not message.text.isdigit():

        await message.answer(
            "❌ Введите ID числом."
        )
        return

    transaction_id = int(message.text)

    user = await get_current_user(message)

    deleted = await (
        TransactionRepository
        .delete_transaction(
            transaction_id,
            user[0]
        )
    )

    if deleted == 0:
        await message.answer(
            "❌ Транзакция не найдена."
        )

        return



    await state.clear()

    await message.answer(
        "✅ Транзакция удалена."
    )

@router.message(
    StateFilter("*"),
    Command("cancel")
)
async def cancel_handler(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "✅ Действие отменено."
    )


