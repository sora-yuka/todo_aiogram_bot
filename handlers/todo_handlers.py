from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from utils.todo_states import ToDoStatesGroup, DetailViewStatesGroup
from utils.todo import Get, Detail, Add
from keyboards.user_keyboard import get_user_keyboard, ReplyKeyboardRemove


class GetTodo:
    async def get_todo_list(self, message: types.Message) -> None:
        await message.answer("Trying to get data...")
        await message.answer(
            text = Get.get_todo_list(message.from_user.username),
            reply_markup=get_user_keyboard()
        )
        
        
class DetailTodo:
    async def ask_point_id(self, message: types.Message) -> None:
        await message.answer(Get.get_todo_list(message.from_user.username))
        if Get.get_todo_list(message.from_user.username) != "Nothing here.":
            await DetailViewStatesGroup.id.set()
            await message.answer(
                "Send me unique point id to get detailed information.", 
                reply_markup=ReplyKeyboardRemove()
            )
        
    async def get_detail_point(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["id"] = message.text
            await message.answer(
                text = Detail.get_detail_point(data["id"], message.from_user.username),
                reply_markup=get_user_keyboard()
            )
        await state.finish()


class PostTodo:
    async def add_point(self, message: types.Message) -> None:
        await message.answer(
            "Let's create todo point! To begin with, send me a point title.",
            reply_markup=ReplyKeyboardRemove()
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
                "Created successfully!", 
                reply_markup=get_user_keyboard()
            )
            await message.answer(
                f"Title: {data['title']}\nDescirption: {data['description']}\nDeadline: {data['deadline']}",
            )
        todo = Add(data["title"], data["description"], data["deadline"])
        todo.add_point_to_list(message.from_user.username)
        await state.finish()
    
    
class UpdateTodo:
    ...
    

def register_todo_handlers(dispatcher: Dispatcher) -> None:
    """ Registering todo handlers """
    dispatcher.register_message_handler(GetTodo().get_todo_list, Text(equals="Get ToDo list"))
    dispatcher.register_message_handler(DetailTodo().ask_point_id, Text(equals="Get detail overview"))
    dispatcher.register_message_handler(DetailTodo().get_detail_point, state=DetailViewStatesGroup.id)
    dispatcher.register_message_handler(PostTodo().add_point, Text(equals="Add point to ToDo list"))
    dispatcher.register_message_handler(PostTodo().load_point_title, state=ToDoStatesGroup.title)
    dispatcher.register_message_handler(PostTodo().load_point_description, state=ToDoStatesGroup.description)
    dispatcher.register_message_handler(PostTodo().load_point_deadline, state=ToDoStatesGroup.deadline)