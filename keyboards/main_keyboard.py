from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text="➕ Доход"),
            KeyboardButton(text="➖ Расход")
        ],

        [
            KeyboardButton(text="📄 Транзакции"),
            KeyboardButton(text="📊 Статистика")
        ],

        [
            KeyboardButton(text="🎯 Цели")
        ]

    ],
    resize_keyboard=True
)