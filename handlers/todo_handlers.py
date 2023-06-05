from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove as close_keyboard
from aiogram.utils.exceptions import MessageTextIsEmpty
from keyboards.user_keyboard import get_user_keyboard
from keyboards.todo_keyboard import get_patch_keyboard
from utils.views import Get, Detail, Add, Patch, Delete
from utils.todo_states import (
    ToDoStatesGroup, DetailViewStatesGroup, PatchStateGroup, 
    TitlePatchState, DescriptionPatchState, DeadlinePatchState,
    DeleteState
)


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
        
        
class DetailTodo(GetTodo):
    async def ask_point_id(self, message: types.Message) -> None:
        await super().get_todo_list(message)
        await message.answer(
            "Send me unique point id to get detailed information.",
            reply_markup = close_keyboard(),
        )
        await DetailViewStatesGroup.id.set()
        
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
                f"<b>Todo:</b> {data['title']}\n<b>Descirption:</b> {data['description']}\n"
                f"<b>Deadline:</b> {data['deadline']}",
                parse_mode="html",
            )
        todo = Add(data["title"], data["description"], data["deadline"])
        todo.add_point_to_list(message.from_user.username)
        await state.finish()
    
    
class PatchTodo(GetTodo):
    async def ask_point_id(self, message: types.Message) -> None:
        await super().get_todo_list(message)
        await message.answer(
                "Send me a unique point id to select and edit.",
                reply_markup = close_keyboard(),
            )
        await PatchStateGroup.id.set()
    
    async def get_point_id(self, message: types.Message, state) -> None:
        global point_id
        async with state.proxy() as data:
            data["id"] = message.text
            point_id = data["id"]
            result = Detail.get_detail_point(
                point_id, message.from_user.username
            )
            await message.answer(
                text = result,
                parse_mode = "html",
                reply_markup = get_patch_keyboard(),
            )
        if result != "There is no such unique id in your Todo-list!":
            await message.answer(
                "What do you want to edit?", 
                reply_markup = get_patch_keyboard()
            )
        else:
            await message.answer(
                "Please, try again.", reply_markup = get_user_keyboard()
            )
        await state.finish()
        
    async def ask_new_title(self, message: types.Message) -> None:
        await message.answer(
            "Good. Now, enter a new title for the point.",
            reply_markup = close_keyboard()
        )
        await TitlePatchState.title.set()
    
    async def ask_new_description(self, message: types.Message) -> None:
        await message.answer(
            "Cool, enter a new description for the point.",
            reply_markup = close_keyboard()
        )
        await DescriptionPatchState.description.set()
        
    async def ask_new_deadline(self, message: types.Message) -> None:
        await message.answer(
            "OK. You can enter a new deadline for the point.",
            reply_markup = close_keyboard()
        )
        await DeadlinePatchState.deadline.set()
        
    async def load_new_title(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["title"] = message.text
            Patch().update_title(point_id, data["title"])
        await message.answer(
            "Updated successfully!", reply_markup = get_user_keyboard()
        )
        await state.finish()
        
    async def load_new_description(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["description"] = message.text
            Patch.update_description(point_id, data["description"])
        await message.answer(
            "Updated successfully!", reply_markup = get_user_keyboard()
        )
        await state.finish()
        
    async def load_new_deadline(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["deadline"] = message.text
            Patch.update_deadline(point_id, data["deadline"])
        await message.answer(
            "Updated successfully!", reply_markup = get_user_keyboard()
        )
        await state.finish()
        
        
class DeleteTodo(GetTodo):
    async def ask_point_id(self, message: types.Message) -> None:
        await super().get_todo_list(message)
        await message.answer(
            "Send me a unique point id to delete id.",
            reply_markup = close_keyboard()
        )
        await DeleteState.id.set()
    
    async def get_point_id(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["id"] = message.text
        result = Detail.get_detail_point(data["id"], message.from_user.username)
            
        if result != "There is no such unique id in your Todo-list!":
            Delete.delete_point(data["id"])
            await message.answer(
                "Deleted successfully!", reply_markup = get_user_keyboard()
            )
        else:
            await message.answer(
                f"{result} Please, try again.", reply_markup = get_user_keyboard()
            )
        await state.finish()
        

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
    dispatcher.register_message_handler(PatchTodo().get_point_id, state=PatchStateGroup.id)
    dispatcher.register_message_handler(PatchTodo().ask_new_title, Text(equals="Title"))
    dispatcher.register_message_handler(PatchTodo().ask_new_description, Text(equals="Description"))
    dispatcher.register_message_handler(PatchTodo().ask_new_deadline, Text(equals="Deadline"))
    dispatcher.register_message_handler(PatchTodo().load_new_title, state=TitlePatchState.title)
    dispatcher.register_message_handler(PatchTodo().load_new_description, state=DescriptionPatchState.description)
    dispatcher.register_message_handler(PatchTodo().load_new_deadline, state=DeadlinePatchState.deadline)
    dispatcher.register_message_handler(DeleteTodo().ask_point_id, Text(equals="Delete point from Todo-list"))
    dispatcher.register_message_handler(DeleteTodo().get_point_id, state=DeleteState.id)