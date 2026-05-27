from datetime import datetime
import aiosqlite

DATABASE_NAME = "finance.db"


class TransactionRepository:

    @staticmethod
    async def add_transaction(
        user_id: int,
        transaction_type: str,
        amount: float,
        category: str
    ):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            await db.execute(
                """
                INSERT INTO transactions
                (user_id, type, amount, category, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    transaction_type,
                    amount,
                    category,
                    datetime.now().strftime("%d.%m.%Y %H:%M")
                )
            )

            await db.commit()

    @staticmethod
    async def get_transactions(user_id: int):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            cursor = await db.execute(
                """
                SELECT type, amount, category, created_at
                FROM transactions
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,)
            )

            transactions = await cursor.fetchall()

            return transactions

    @staticmethod
    async def get_statistics(user_id: int):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            income_cursor = await db.execute(
                """
                SELECT SUM(amount)
                FROM transactions
                WHERE user_id = ?
                AND type = 'income'
                """,
                (user_id,)
            )

            expense_cursor = await db.execute(
                """
                SELECT SUM(amount)
                FROM transactions
                WHERE user_id = ?
                AND type = 'expense'
                """,
                (user_id,)
            )

            income_result = await income_cursor.fetchone()
            expense_result = await expense_cursor.fetchone()

            income = income_result[0] or 0
            expense = expense_result[0] or 0

            balance = income - expense

            return {
                "income": income,
                "expense": expense,
                "balance": balance
            }

    @staticmethod
    async def get_expense_categories(user_id: int):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            cursor = await db.execute(
                """
                SELECT category, SUM(amount)

                FROM transactions

                WHERE user_id = ?
                AND type = 'expense'

                GROUP BY category

                ORDER BY SUM(amount) DESC
                """,
                (user_id,)
            )

            categories = await cursor.fetchall()

            return categories