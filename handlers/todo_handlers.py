from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove as close_keyboard
from aiogram.utils.exceptions import MessageTextIsEmpty
from keyboards.user_keyboard import (
    get_user_keyboard, get_user_inlinekeyboard, inline_interrupt
)
from keyboards.todo_keyboard import get_patch_keyboard
from utils.views import Get, Detail, Add, Patch, Delete
from utils.todo_states import (
    ToDoStatesGroup, DetailViewStatesGroup, PatchStateGroup, 
    TitlePatchState, DescriptionPatchState, DeadlinePatchState,
)

            
class GetTodo:
    async def get_todo_list(self, message: types.Message) -> None:
        await message.answer("Trying to get data...")
        try:
            await message.answer_photo(
                photo = "https://backlog.com/wp-blog-app/uploads/sites/6/2019/11/7dd9a07b407f4382a535340e39ab24e2.png",
                caption = Get.get_todo_list(message.from_user.username),
                parse_mode = "html",
                reply_markup = get_user_keyboard()
            )
        except MessageTextIsEmpty as _ex:
            await message.answer("Todo-list is empty.")
            
        await message.answer(
            "Send me unique point id to get detailed information.",
            reply_markup = inline_interrupt(),
        )
        await DetailViewStatesGroup.id.set()
        
    async def interrupt_detail_view(self, callback: types.CallbackQuery, state) -> None:
        if callback.data == "cancel":
            await callback.answer("You interrupted detailed view!")
            await state.finish()
        
    async def get_detail_point(self, message: types.Message, state) -> None:
        async with state.proxy() as data:
            data["id"] = message.text   
        detailed_view = Detail.get_detail_point(
            data["id"], message.from_user.username
        )
        
        if not detailed_view.description == "Done":
            await message.answer_photo(
                photo = "https://assets.st-note.com/production/uploads/images/51552657/123ed2281350328a8189fb4a4a11a296.png",
                caption = detailed_view,
                parse_mode="html",
                reply_markup = get_user_inlinekeyboard(),
            )
        else:
            await message.answer_photo(
                    photo = "https://lychee-redmine.jp/wp-content/uploads/2022/10/24875664_m_0.jpg",
                    caption = detailed_view,
                    parse_mode="html",
                    reply_markup = get_user_inlinekeyboard(),
                )
        await message.answer(
            "Following actions are available to you 😉", reply_markup = get_user_keyboard()
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
            await message.answer_photo(
                photo = "https://alexaguy.com/wp-content/uploads/2018/09/94735-istock-863607936.jpg",
                caption = f"<b>Todo:</b> {data['title']}\n<b>Descirption:</b> {data['description']}\n"
                f"<b>Deadline:</b> {data['deadline']}",
                parse_mode = "html",
                reply_markup = get_user_keyboard()
            )
        todo = Add(data["title"], data["description"], data["deadline"])
        todo.add_point_to_list(message.from_user.username)
        await state.finish()
        

class PatchDeleteDoneTodo:
    async def point_preferences(self, callback: types.CallbackQuery) -> None:
        global point_id
        point_id = callback.message.caption.split("Unique id:")[1].split()[0]
            
        if callback.data == "edit":
            await callback.message.answer(
                "What do you want to edit?", reply_markup = get_patch_keyboard()
            )
            await callback.answer("You choose edit point")
            return point_id
            
        elif callback.data == "delete":
            try:
                Delete.delete_point(point_id, callback.from_user.username)
                await callback.message.answer(
                    "Deleted successfully!", reply_markup = get_user_keyboard()
                )
            except IndexError:
                await callback.answer("Something get wrong!")
        else:
            Patch.update_description(point_id, "Done")
            Patch.update_deadline(point_id, "Done")
            await callback.message.answer_photo(
                photo = "https://lychee-redmine.jp/wp-content/uploads/2022/10/24875664_m_0.jpg",
                caption = Detail.get_detail_point(point_id, callback.from_user.username),
                parse_mode="html",
                reply_markup = get_user_keyboard(),
            )
            await callback.answer("You completed point!")


class PatchingTodo:
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
            

def register_todo_handlers(dispatcher: Dispatcher) -> None:
    """ Registering todo handlers """
    dispatcher.register_message_handler(GetTodo().get_todo_list, Text(equals="Get points"))
    dispatcher.register_callback_query_handler(GetTodo().interrupt_detail_view, state=DetailViewStatesGroup.id)
    dispatcher.register_message_handler(GetTodo().get_detail_point, state=DetailViewStatesGroup.id)
    dispatcher.register_message_handler(PostTodo().add_point, Text(equals="Add point"))
    dispatcher.register_message_handler(PostTodo().load_point_title, state=ToDoStatesGroup.title)
    dispatcher.register_message_handler(PostTodo().load_point_description, state=ToDoStatesGroup.description)
    dispatcher.register_message_handler(PostTodo().load_point_deadline, state=ToDoStatesGroup.deadline)
    dispatcher.register_callback_query_handler(PatchDeleteDoneTodo().point_preferences)
    dispatcher.register_message_handler(PatchingTodo().ask_new_title, Text(equals="Title"))
    dispatcher.register_message_handler(PatchingTodo().ask_new_description, Text(equals="Description"))
    dispatcher.register_message_handler(PatchingTodo().ask_new_deadline, Text(equals="Deadline"))
    dispatcher.register_message_handler(PatchingTodo().load_new_title, state=TitlePatchState.title)
    dispatcher.register_message_handler(PatchingTodo().load_new_description, state=DescriptionPatchState.description)
    dispatcher.register_message_handler(PatchingTodo().load_new_deadline, state=DeadlinePatchState.deadline)