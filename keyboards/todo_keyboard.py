from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def get_patch_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton("Title"), KeyboardButton("Description"), 
                KeyboardButton("Deadline"),
            ]
        ]
    )
    
    return main_keyboard

def interrupt_patch_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton("Cancel")
            ]
        ]
    )
    
    return main_keyboard

def delete_keyboard() -> InlineKeyboardMarkup:
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Delete", callback_data="delete")
            ]
        ]
    )
    
    return main_keyboard