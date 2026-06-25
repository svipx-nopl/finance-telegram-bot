from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from utils.auth import check_user_registered

from repositories.goal_repository import GoalRepository
from repositories.transaction_repository import TransactionRepository

from utils.validators import validate_amount

router = Router()


@router.message(Command("set_goal"))
async def set_goal_handler(message: Message):

    args = message.text.split()

    if len(args) < 3:

        await message.answer(
            "Использование:\n"
            "/set_goal сумма описание"
        )

        return

    is_valid, result = validate_amount(args[1])

    if not is_valid:
        await message.answer(result)
        return

    target_amount = result

    description = " ".join(args[2:])

    await GoalRepository.add_goal(
        user_id=message.from_user.id,
        target_amount=target_amount,
        description=description
    )

    await message.answer(
        f"🎯 Цель добавлена:\n\n"
        f"💰 Сумма: {target_amount} ₽\n"
        f"📝 Описание: {description}"
    )


@router.message(Command("goals"))
async def goals_handler(message: Message):

    goals = await GoalRepository.get_goals(
        message.from_user.id
    )

    if not goals:

        await message.answer(
            "У вас пока нет целей"
        )

        return

    stats = await TransactionRepository.get_statistics(
        message.from_user.id
    )

    current_balance = stats["balance"]

    text = "🎯 Ваши цели:\n\n"

    for goal in goals:

        target_amount, description = goal

        if target_amount <= 0:

            progress = 0

        else:

            progress = min(
                (current_balance / target_amount) * 100,
                100
            )

        if progress > 100:
            progress = 100

        text += (
            f"📝 {description}\n"
            f"💰 Цель: {target_amount} ₽\n"
            f"📈 Прогресс: {progress:.1f}%\n"
            f"💵 Накоплено: {current_balance} ₽\n\n"
        )

        if current_balance >= target_amount:

            text += (
                "✅ Цель достигнута!\n\n"
            )

    await message.answer(text)


@router.message(F.text == "🎯 Цели")
async def goals_button_handler(message: Message):


    goals = await GoalRepository.get_goals(
        message.from_user.id
    )

    if not goals:

        await message.answer(
            "У вас пока нет целей\n\n"
            "Пример:\n"
            "/set_goal 100000 Отпуск"
        )

        return

    stats = await TransactionRepository.get_statistics(
        message.from_user.id
    )

    current_balance = stats["balance"]

    text = "🎯 Ваши цели:\n\n"

    for goal in goals:

        target_amount, description = goal

        if target_amount <= 0:

            progress = 0

        else:

            progress = min(
                (current_balance / target_amount) * 100,
                100
            )

        if progress > 100:
            progress = 100

        text += (
            f"📝 {description}\n"
            f"💰 Цель: {target_amount} ₽\n"
            f"📈 Прогресс: {progress:.1f}%\n"
            f"💵 Накоплено: {current_balance} ₽\n\n"
        )

        if current_balance >= target_amount:

            text += (
                "✅ Цель достигнута!\n\n"
            )

    await message.answer(text)