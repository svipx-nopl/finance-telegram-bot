from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.types import FSInputFile
from utils.auth import check_user_registered

from utils.charts import create_expense_chart

from repositories.transaction_repository import (
    TransactionRepository
)

router = Router()


@router.message(Command("statistics"))
async def statistics_handler(message: Message):

    stats = await TransactionRepository.get_statistics(
        message.from_user.id
    )

    categories = await (
        TransactionRepository
        .get_expense_categories(
            message.from_user.id
        )
    )

    total_expense = stats["expense"]

    text = (
        "📊 Статистика:\n\n"

        f"💰 Доходы: {stats['income']} ₽\n"
        f"💸 Расходы: {stats['expense']} ₽\n"
        f"💵 Баланс: {stats['balance']} ₽\n\n"
    )

    if categories:

        text += "📂 Категории расходов:\n\n"

        for category, amount in categories:

            percent = (
                amount / total_expense
            ) * 100

            text += (
                f"📌 {category} — "
                f"{amount} ₽ "
                f"({percent:.1f}%)\n"
            )

        categories_dict = {
            category: amount
            for category, amount in categories
        }

        chart_path = create_expense_chart(
            categories_dict
        )

        if chart_path:

            photo = FSInputFile(chart_path)

            await message.answer_photo(
                photo=photo,
                caption="📊 График расходов"
            )

    await message.answer(text)


@router.message(F.text == "📊 Статистика")
async def statistics_button_handler(message: Message):

    if not await check_user_registered(message):
        return

    await statistics_handler(message)

