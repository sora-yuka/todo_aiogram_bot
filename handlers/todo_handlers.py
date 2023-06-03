from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from utils.todo import Get, Add

async def get_todo_list(message: types.Message) -> None:
    await message.answer(
        text = Get().get_todo_list(),
    )

async def add_todo_point(message: types.Message) -> None:
    await message.answer(
        "Input todo title."
    )
    Add().add_point_to_list(message.text)
    

def register_todo_handlers(dispatcher: Dispatcher) -> None:
    """ Register todo handlers """
    dispatcher.register_message_handler(get_todo_list, Text(equals="Get ToDo list"))
    dispatcher.register_message_handler(add_todo_point, Text(equals="Add point to ToDo list"))