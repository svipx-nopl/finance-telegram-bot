import aiosqlite
from config import DATABASE_NAME

class TransactionRepository:

    @staticmethod
    async def add_transaction(user_id, t_type, amount, category):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            await db.execute(
                """
                INSERT INTO transactions
                (user_id, type, amount, category)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, t_type, amount, category)
            )
            await db.commit()

    @staticmethod
    async def get_transactions(user_id):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            cursor = await db.execute(
                "SELECT * FROM transactions WHERE user_id=?",
                (user_id,)
            )
            return await cursor.fetchall()

    @staticmethod
    async def get_transactions_by_period(user_id, start_date):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            cursor = await db.execute(
                """
                SELECT * FROM transactions
                WHERE user_id=? AND created_at>=?
                ORDER BY created_at DESC
                """,
                (user_id, start_date)
            )
            return await cursor.fetchall()