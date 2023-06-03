from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def get_user_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton("Get ToDo list"), KeyboardButton("Add point to ToDo list"), 
                KeyboardButton("Edit ToDo list"), KeyboardButton("Delete point from ToDo list")
            ]
        ]
    )
    
    return main_keyboard