from aiogram import types, Dispatcher
from keyboards.user_keyboard import get_user_keyboard


async def command_start(message: types.Message) -> None:
    await message.answer(
        f"Welcome to TodoBot, your personal productivity companion right at your fingertips!",
        reply_markup = get_user_keyboard()
    )
    await message.delete()
    
    
def register_user_handlers(dispatcher: Dispatcher):
    """ Register user handlers """
    dispatcher.register_message_handler(command_start, commands=["start"])