from aiogram.fsm.state import State, StatesGroup


class AddExpenseState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()


class AddIncomeState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()