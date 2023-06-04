from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove as close_keyboard
from aiogram.utils.exceptions import MessageTextIsEmpty
from utils.todo_states import ToDoStatesGroup, DetailViewStatesGroup
from utils.todo import Get, Detail, Add, Patch
from keyboards.user_keyboard import get_user_keyboard
from keyboards.todo_keyboard import get_patch_keyboard


class GetTodo:
    async def get_todo_list(self, message: types.Message) -> None:
        await message.answer("Trying to get data...")
        try:
            await message.answer(
                text = Get.get_todo_list(message.from_user.username),
                parse_mode="html",
                reply_markup = get_user_keyboard(),
            )
        except MessageTextIsEmpty as _ex:
            await message.answer("Todo-list is empty.")
        
        
class DetailTodo:
    async def ask_point_id(self, message: types.Message) -> None:
        try:
            await message.answer(
                Get.get_todo_list(message.from_user.username),
                parse_mode="html")
            await message.answer(
                "Send me unique point id to get detailed information.",
                reply_markup = close_keyboard(),
            )
            await DetailViewStatesGroup.id.set()
        except MessageTextIsEmpty as _ex:
            await message.answer("Todo-list is empty.")
        
    async def get_detail_point(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["id"] = message.text
            await message.answer(
                text = Detail.get_detail_point(data["id"], message.from_user.username),
                parse_mode="html",
                reply_markup = get_user_keyboard(),
            )
        await state.finish()


class PostTodo:
    async def add_point(self, message: types.Message) -> None:
        await message.answer(
            "Let's create todo point! To begin with, send me a point title.",
            reply_markup=close_keyboard(),
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
                reply_markup = get_user_keyboard(),
            )
            await message.answer(
                f"<b>Title:</b> {data['title']}\n<b>Descirption:</b> {data['description']}\n"
                f"<b>Deadline:</b> {data['deadline']}",
                parse_mode="html",
            )
        todo = Add(data["title"], data["description"], data["deadline"])
        todo.add_point_to_list(message.from_user.username)
        await state.finish()
    
    
class PatchTodo:
    async def ask_point_id(self, message: types.Message) -> None:
        try:
            await message.answer(
                Get.get_todo_list(message.from_user.username),
                parse_mode="html",
            )
            await message.answer(
                "Send me unique id to edit point",
                reply_markup = close_keyboard(),
            )
            await DetailViewStatesGroup.id.set()
        except MessageTextIsEmpty as _ex:
            await message.answer("Todo-list is empty.")
    
    async def get_patch_id(self, message: types.Message, state) -> None:
        global point_id
        async with state.proxy() as data:
            data["id"] = message.text
            point_id = data["id"]
            await message.answer(
                text = Detail.get_detail_point(data["id"], message.from_user.username),
                parse_mode = "html",
                reply_markup = close_keyboard(),
            )
        await state.finish()
        
#$  ^^^^^^^^^^
#@ got point id 
        
    async def patch_preferences(message: types.Message) -> None:
        await message.answer(
            "What do you want to edit?", 
            reply_markup = get_patch_keyboard()
        )

#$  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#@ asking for prefences: title, description or deadline
        
    async def ask_new_title(message: types.Message) -> None:
        message.answer(
            "Type new title for point.",
            reply_markup = close_keyboard()
        )
        await ToDoStatesGroup.title.set()
    
    async def load_new_title(message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["title"] = title
        Patch.update_title(point_id, data["title"])
        await state.finish()
        
#$  ^^^^^^^^^^
#@ title loaded
        

def register_todo_handlers(dispatcher: Dispatcher) -> None:
    """ Registering todo handlers """
    dispatcher.register_message_handler(GetTodo().get_todo_list, Text(equals="Get Todo-list"))
    dispatcher.register_message_handler(DetailTodo().ask_point_id, Text(equals="Get detailed overview"))
    dispatcher.register_message_handler(DetailTodo().get_detail_point, state=DetailViewStatesGroup.id)
    dispatcher.register_message_handler(PostTodo().add_point, Text(equals="Add point to Todo-list"))
    dispatcher.register_message_handler(PostTodo().load_point_title, state=ToDoStatesGroup.title)
    dispatcher.register_message_handler(PostTodo().load_point_description, state=ToDoStatesGroup.description)
    dispatcher.register_message_handler(PostTodo().load_point_deadline, state=ToDoStatesGroup.deadline)
    dispatcher.register_message_handler(PatchTodo().ask_point_id, Text(equals="Edit point from Todo-list"))
    dispatcher.register_message_handler(PatchTodo().get_patch_id, state=DetailViewStatesGroup.id)
    dispatcher.register_message_handler(Patch().ask_new_title, Text(equals="Title"))
    