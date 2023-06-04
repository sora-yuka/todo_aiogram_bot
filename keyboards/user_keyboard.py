from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def get_user_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton("Get Todo-list"), KeyboardButton("Get detailed overview"), 
                KeyboardButton("Add point to Todo-list"), KeyboardButton("Edit point from Todo-list"), 
                KeyboardButton("Delete point from Todo-list"),
            ]
        ]
    )
    
    return main_keyboard