from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class AddTransactionState(StatesGroup):

    waiting_for_amount = State()

    waiting_for_category = State()