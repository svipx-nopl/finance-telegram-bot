from repositories.user_repository import UserRepository

class UserService:

    @staticmethod
    async def register_user(telegram_id, username):
        user = await UserRepository.get_user_by_telegram_id(telegram_id)

        if user:
            return False

        await UserRepository.create_user(telegram_id, username)
        return True