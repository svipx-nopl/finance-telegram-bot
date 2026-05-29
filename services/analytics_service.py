from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from collections import defaultdict

class AnalyticsService:

    @staticmethod
    async def get_statistics(telegram_id):

        user = await UserRepository.get_user_by_telegram_id(telegram_id)

        transactions = await TransactionRepository.get_transactions(user[0])

        total_income = 0
        total_expense = 0

        categories = defaultdict(float)

        for transaction in transactions:

            transaction_id, t_type, amount, category, created_at = transaction

            if t_type == "income":
                total_income += amount
            else:
                total_expense += amount
                categories[category] += amount

        balance = total_income - total_expense

        return {
            "income": total_income,
            "expense": total_expense,
            "balance": balance,
            "categories": dict(categories)
        }