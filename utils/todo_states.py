from aiogram.dispatcher.filters.state import StatesGroup, State


class ToDoStatesGroup(StatesGroup):
    title = State()
    description = State()
    # deadline = State()