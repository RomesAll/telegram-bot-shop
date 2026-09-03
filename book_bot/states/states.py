from aiogram.fsm.state import State, StatesGroup

class BookStates(StatesGroup):
    """Состояния для бота"""
    reading = State()
    purchasing = State()
    browsing = State()