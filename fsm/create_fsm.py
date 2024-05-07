from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup

class FSMReadSolve(StatesGroup):
    choose_action = State()
    read_text = State()
    solve_task = State()
    form = State()
