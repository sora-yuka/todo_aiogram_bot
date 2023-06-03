from aiogram.dispatcher.filters.state import StatesGroup, State


class ToDoStatesGroup(StatesGroup):
    """ Todo state declaration """
    title = State()
    description = State()
    deadline = State()