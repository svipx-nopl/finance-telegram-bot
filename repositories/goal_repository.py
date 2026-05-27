import aiosqlite
from config import DATABASE_NAME

class GoalRepository:

    @staticmethod
    async def create_goal(user_id, amount, description):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            await db.execute(
                """
                INSERT INTO goals (user_id, target_amount, description)
                VALUES (?, ?, ?)
                """,
                (user_id, amount, description)
            )
            await db.commit()

    @staticmethod
    async def get_goals(user_id):
        async with aiosqlite.connect(DATABASE_NAME) as db:
            cursor = await db.execute(
                "SELECT * FROM goals WHERE user_id=?",
                (user_id,)
            )
            return await cursor.fetchall()