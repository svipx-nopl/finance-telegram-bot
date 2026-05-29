from repositories.user_repository import UserRepository


async def check_user_registered(message):

    user = await UserRepository.get_user_by_telegram_id(
        message.from_user.id
    )

    if not user:

        await message.answer(
            "❌ Сначала зарегистрируйтесь:\n"
            "/register"
        )

        return False

    return True


async def get_current_user(message):

    return await UserRepository.get_user_by_telegram_id(
        message.from_user.id
    )