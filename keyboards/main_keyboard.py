from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Доход"),
            KeyboardButton(text="➖ Расход")
        ],
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="🎯 Цели")
        ]
    ],
    resize_keyboard=True
)