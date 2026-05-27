from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F


router = Router()


@router.message(Command("set_goal"))
async def set_goal_handler(message: Message):
    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        await message.answer(
            "Использование: /set_goal сумма описание"
        )
        return

    amount = args[1]
    description = args[2]

    await message.answer(
        f"Цель установлена: {description} | {amount} ₽"
    )


@router.message(F.text == "🎯 Цели")
async def goals_button_handler(message: Message):
    await message.answer(
        "Используйте:\n/set_goal сумма описание"
    )