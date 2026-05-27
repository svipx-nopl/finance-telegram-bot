from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import matplotlib.pyplot as plt
from aiogram.types import FSInputFile

from repositories.transaction_repository import TransactionRepository

router = Router()


@router.message(Command("statistics"))
async def statistics_handler(message: Message):

    stats = await TransactionRepository.get_statistics(
        message.from_user.id
    )

    categories = await TransactionRepository.get_expense_categories(
        message.from_user.id
    )

    text = (
        "📊 Статистика:\n\n"

        f"💰 Доходы: {stats['income']} ₽\n"
        f"💸 Расходы: {stats['expense']} ₽\n"
        f"💵 Баланс: {stats['balance']} ₽\n\n"
    )

    if categories:

        text += "📂 Категории расходов:\n\n"

        total_expense = stats["expense"]

        for category, amount in categories:

            percent = (
                amount / total_expense
            ) * 100

            text += (
                f"📌 {category} — "
                f"{amount} ₽ "
                f"({percent:.1f}%)\n"
            )

    if categories:

        labels = []
        amounts = []

        for category, amount in categories:
            labels.append(category)
            amounts.append(amount)

        plt.figure(figsize=(7, 7))

        plt.pie(
            amounts,
            labels=labels,
            autopct='%1.1f%%'
        )

        plt.title("Структура расходов")

        chart_path = "charts/expenses_pie.png"

        plt.savefig(chart_path)

        plt.close()

        photo = FSInputFile(chart_path)

        await message.answer_photo(
            photo=photo,
            caption="📊 График расходов"
        )


    await message.answer(text)


@router.message(F.text == "📊 Статистика")
async def statistics_button_handler(message: Message):

    stats = await TransactionRepository.get_statistics(
        message.from_user.id
    )

    categories = await TransactionRepository.get_expense_categories(
        message.from_user.id
    )

    text = (
        "📊 Статистика:\n\n"

        f"💰 Доходы: {stats['income']} ₽\n"
        f"💸 Расходы: {stats['expense']} ₽\n"
        f"💵 Баланс: {stats['balance']} ₽\n\n"
    )

    if categories:

        text += "📂 Категории расходов:\n\n"

        total_expense = stats["expense"]

        for category, amount in categories:

            percent = (
                amount / total_expense
            ) * 100

            text += (
                f"📌 {category} — "
                f"{amount} ₽ "
                f"({percent:.1f}%)\n"
            )


        if categories:

            labels = []
            amounts = []

            for category, amount in categories:

                labels.append(category)
                amounts.append(amount)

            plt.figure(figsize=(7, 7))

            plt.pie(amounts, labels=labels, autopct='%1.1f%%')

            plt.title("Структура расходов")

            chart_path = "charts/expenses_pie.png"

            plt.savefig(chart_path)

            photo = FSInputFile(chart_path)

            await message.answer_photo(photo=photo,captioon="📊 График расходов")

    await message.answer(text)