from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def order_cancel():
    cancel = KeyboardButton('❌Отмена')
    menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    menu.add(cancel)
    return menu
