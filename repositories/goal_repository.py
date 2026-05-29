import aiosqlite
from config import DATABASE_NAME


class GoalRepository:

    @staticmethod
    async def add_goal(
        user_id: int,
        target_amount: float,
        description: str
    ):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            await db.execute(
                """
                INSERT INTO goals
                (user_id, target_amount, description)
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    target_amount,
                    description
                )
            )

            await db.commit()

    @staticmethod
    async def get_goals(user_id: int):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            cursor = await db.execute(
                """
                SELECT id, target_amount, description
                FROM goals
                WHERE user_id = ?
                """,
                (user_id,)
            )

            goals = await cursor.fetchall()

            return goals

    @staticmethod
    async def delete_goal(
        goal_id: int,
        user_id: int
    ):

        async with aiosqlite.connect(DATABASE_NAME) as db:

            cursor = await db.execute(
                """
                DELETE FROM goals
                WHERE id = ?
                AND user_id = ?
                """,
                (
                    goal_id,
                    user_id
                )
            )

            await db.commit()

            return cursor.rowcount