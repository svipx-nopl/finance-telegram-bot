from repositories.goal_repository import GoalRepository
from services.analytics_service import AnalyticsService
from repositories.user_repository import UserRepository

class GoalService:

    @staticmethod
    async def create_goal(telegram_id, amount, description):

        user = await UserRepository.get_user_by_telegram_id(telegram_id)

        await GoalRepository.create_goal(
            user[0],
            amount,
            description
        )

    @staticmethod
    async def get_goal_progress(telegram_id):

        user = await UserRepository.get_user_by_telegram_id(telegram_id)

        goals = await GoalRepository.get_goals(user[0])

        stats = await AnalyticsService.get_statistics(telegram_id)

        balance = stats["balance"]

        result = []

        for goal in goals:
            _, _, target_amount, description, _ = goal

            progress = min((balance / target_amount) * 100, 100)

            result.append({
                "description": description,
                "target": target_amount,
                "balance": balance,
                "progress": progress
            })

        return result