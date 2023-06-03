from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from utils.todo_states import ToDoStatesGroup
from utils.todo import Get, Add
from keyboards.user_keyboard import get_user_keyboard

class GetTodo:
    async def get_todo_list(self, message: types.Message) -> None:
        await message.answer("Trying to get data...")
        await message.answer(
            text = Get.get_todo_list(),
        )


class PostTodo:
    async def add_todo_point(self, message: types.Message) -> None:
        await message.answer(
            "Let's create todo point! To begin with, send me a point title."
        )
        await ToDoStatesGroup.title.set()
        
    async def load_point_title(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["title"] = message.text
        await message.answer("Next, send me a point description.")
        await ToDoStatesGroup.next()
        
    async def load_point_description(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["description"] = message.text
        await message.answer("Then, send me deadline of your point.")
        await ToDoStatesGroup.next()
    
    async def load_point_deadline(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["deadline"] = message.text
            await message.answer(
                f"Title: {data['title']}\nTo do: {data['description']}\nDeadline: {data['deadline']}"
            )
        todo = Add(data["title"], data["description"], data["deadline"])
        todo.add_point_to_list()
        await message.answer("Created successfully!", reply_markup=get_user_keyboard())
        await state.finish()
    

def register_todo_handlers(dispatcher: Dispatcher) -> None:
    """ Registering todo handlers """
    dispatcher.register_message_handler(GetTodo().get_todo_list, Text(equals="Get ToDo list"))
    dispatcher.register_message_handler(PostTodo().add_todo_point, Text(equals="Add point to ToDo list"))
    dispatcher.register_message_handler(PostTodo().load_point_title, state=ToDoStatesGroup.title)
    dispatcher.register_message_handler(PostTodo().load_point_description, state=ToDoStatesGroup.description)
    dispatcher.register_message_handler(PostTodo().load_point_deadline, state=ToDoStatesGroup.deadline)