from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def terms_of_use_menu():
    terms_of_use_accept = InlineKeyboardButton('Хочу подключить 👌', callback_data='accept_terms_of_use')
    menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu.add(terms_of_use_accept)
    return menu
