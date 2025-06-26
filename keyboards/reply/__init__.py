from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def order_cancel():
    cancel = KeyboardButton('❌Отмена')
    menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    menu.add(cancel)
    return menu

