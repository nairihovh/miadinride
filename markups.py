from aiogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
import aiogram

markup_remove_with_back = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="Հետ")]]
    )

markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[
        KeyboardButton(text="Գնում եմ, կտանեմ"),
        KeyboardButton(text="Ցանկանում եմ գնալ")
    ]]
)


def create_inline_markups(data):
    data = str(data)
    markup_want_to_go = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Գնում եմ", callback_data=data)]]
    )

    markup_is_going = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Կտանեմ", callback_data=data)]]
    )
    return markup_want_to_go, markup_is_going

markup_apply_reject = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[
        KeyboardButton(text="Հաստատել"),
        KeyboardButton(text="Մերժել/Ջնջել"),
        KeyboardButton(text="Հետ")
    ]]
)