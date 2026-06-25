import asyncio
from aiogram import Bot, Dispatcher, F

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def debug(message):
    print("🔥 MESSAGE RECEIVED:", message.text)
    await message.answer("OK")

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())