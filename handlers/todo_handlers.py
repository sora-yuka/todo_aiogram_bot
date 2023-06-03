from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from utils.todo import Get, Add
from utils.todo_states import ToDoStatesGroup

async def get_todo_list(message: types.Message) -> None:
    await message.answer(
        text = Get().get_todo_list(),
    )

async def add_todo_point(message: types.Message) -> None:
    await message.answer(
        "Let's create todo point! To begin with, send me a point title."
    )
    await ToDoStatesGroup.title.set()
    
async def load_point_title(message: types.Message, state) -> None:
    async with state.proxy() as data:
        data["title"] = message.text
    
    await message.answer("Next, send me a point description.")
    await ToDoStatesGroup.next()
    
async def load_point_description(message: types.Message, state) -> None:
    async with state.proxy() as data:
        data["description"] = message.text
        
        await message.answer(f"Title: {data['title']}\nTo do: {data['description']}")
    
    await message.answer("Created successfully!")
    await state.finish()
    

def register_todo_handlers(dispatcher: Dispatcher) -> None:
    """ Registering todo handlers """
    dispatcher.register_message_handler(get_todo_list, Text(equals="Get ToDo list"))
    dispatcher.register_message_handler(add_todo_point, Text(equals="Add point to ToDo list"))
    dispatcher.register_message_handler(load_point_title, state=ToDoStatesGroup.title)
    dispatcher.register_message_handler(load_point_description, state=ToDoStatesGroup.description)