from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, 
    InlineKeyboardButton, InlineKeyboardMarkup
)


def get_user_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton("Get points"), KeyboardButton("Add point"),
            ]
        ]
    )
    
    return main_keyboard

def get_user_inlinekeyboard() -> InlineKeyboardMarkup:
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton("Edit", callback_data="edit"),
                InlineKeyboardButton("Done", callback_data="done"),
                InlineKeyboardButton("Delete", callback_data="delete"),
            ]
        ]
    )
    
    return main_keyboard

def inline_interrupt() -> InlineKeyboardMarkup:
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton("Cancel", callback_data="cancel")
            ]
        ]
    )
    
    return main_keyboard