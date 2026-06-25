from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
        ],

        [
            KeyboardButton(text="🗑 Удалить транзакцию")
        ],

        [
            KeyboardButton(text="🚪 Выйти")
        ]
    ],
    resize_keyboard=True
)