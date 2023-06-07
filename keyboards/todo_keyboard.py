from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_patch_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton("Title"), KeyboardButton("Description"), 
                KeyboardButton("Deadline"), KeyboardButton("Cancel")
            ]
        ]
    )
    
    return main_keyboard