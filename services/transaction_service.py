from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository

class TransactionService:

    @staticmethod
    async def add_income(telegram_id, amount, category):
        user = await UserRepository.get_user_by_telegram_id(telegram_id)

        await TransactionRepository.add_transaction(
            user[0],
            "income",
            amount,
            category
        )

    @staticmethod
    async def add_expense(telegram_id, amount, category):
        user = await UserRepository.get_user_by_telegram_id(telegram_id)

        await TransactionRepository.add_transaction(
            user[0],
            "expense",
            amount,
            category
        )