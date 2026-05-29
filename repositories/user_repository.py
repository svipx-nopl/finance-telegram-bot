import aiosqlite
from config import DATABASE_NAME

class UserRepository:

    @staticmethod
    async def create_user(telegram_id, username):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            await db.execute(
                "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
                (telegram_id, username)
            )
            await db.commit()

    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            cursor = await db.execute(
                "SELECT * FROM users WHERE telegram_id=?",
                (telegram_id,)
            )
            return await cursor.fetchone()

    @staticmethod
    async def delete_user(telegram_id):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            cursor = await db.execute(
                """
                DELETE FROM users
                WHERE telegram_id = ?
                """,
                (telegram_id,)
            )

            await db.commit()

            return cursor.rowcount