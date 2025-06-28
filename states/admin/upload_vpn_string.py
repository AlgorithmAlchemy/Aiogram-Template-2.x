from data import config
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, bot

from loader import dp, bot
import asyncio
import logging
import random
import string
from datetime import date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile, ContentTypes

from models.sqlite3_creator import db, connect
from loader import dp, bot


class UploadState(StatesGroup):
    UploadDataState = State()


# Обработчик команды /up_3d
@dp.message_handler(chat_id=config.OWNER, regexp="up_[0-9]2?(m|d)", chat_type='private')
async def start_upload_data(message: types.Message, state: FSMContext):
    message_text = message.text.replace('/', '')
    if message_text == 'up_3d':
        time_date = 'region_3d'
    elif message_text == 'up_1m':
        time_date = 'region_1m'
    elif message_text == 'up_3m':
        time_date = 'region_3m'
    elif message_text == 'up_6m':
        time_date = 'region_6m'
    elif message_text == 'up_12m':
        time_date = 'region_12m'
    else:
        await message.answer('Ошибка можно загрузить только up_3d/1m/3m/6m/12m')
        return

    await state.update_data(time_date=time_date)  # Сохраняем выбранную дату работы

    # Создание inline кнопок для выбора страны (ячейки) базы данных
    keyboard = types.InlineKeyboardMarkup()
    # keyboard.add(types.InlineKeyboardButton("Finland", callback_data="finland"))
    # keyboard.add(types.InlineKeyboardButton("Kazakhstan", callback_data="kazakhstan"))
    # keyboard.add(types.InlineKeyboardButton("Germany", callback_data="germany"))
    # keyboard.add(types.InlineKeyboardButton("Austria", callback_data="austria"))
    keyboard.add(types.InlineKeyboardButton("Russia", callback_data="russia"))
    # keyboard.add(types.InlineKeyboardButton("India", callback_data="india"))
    keyboard.add(types.InlineKeyboardButton("Netherlands", callback_data="netherlands"))
    # keyboard.add(types.InlineKeyboardButton("USA", callback_data="usa"))

    await message.answer("Выберите страну (ячейку) "
                         "\nдля загрузки данных:", reply_markup=keyboard)

    # Установка состояния UploadDataState
    await UploadState.UploadDataState.set()


# Обработчик выбора страны
@dp.callback_query_handler(lambda c: c.data in ["russia", "netherlands"], state=UploadState.UploadDataState)
async def process_select_country(callback_query: types.CallbackQuery, state: FSMContext):
    country = callback_query.data
    await state.update_data(country=country)  # Сохраняем выбранную страну

    await callback_query.answer()  # Отвечаем на запрос пользователя
    await callback_query.message.answer("Введите данные для загрузки в базу данных(можно пачкой) "
                                        "с отступом(кнопка enter) - на клаве")


# Обработчик ввода данных
@dp.message_handler(state=UploadState.UploadDataState, chat_type='private')
async def process_data(message: types.Message, state: FSMContext):
    data = message.text.strip()
    check_string = 'ss://'
    if data.startswith(check_string):
        country_data = (await state.get_data())["country"]
        time_date = (await state.get_data())["time_date"]

        vpn_strings = message.text.splitlines()
        for vpn_string in vpn_strings:
            if vpn_string and vpn_string.startswith(check_string):
                print(vpn_string)

                # SQL-запрос для вставки данных
                sql_query = f"INSERT INTO {time_date}({country_data}) VALUES (?)"

                # Выполнение SQL-запроса
                db.execute(sql_query, ('Https://s3.amazonaws.com/outline-vpn/invite.html#' +
                                       vpn_string,))
                db.commit()

        await message.answer(f"Данные успешно загружены в страну {country_data}:"
                             f"\n\n<code>{message.text}</code>", parse_mode='HTML')
        await state.finish()  # Завершение состояния
    else:
        await message.answer("Некорректный формат данных. Введите данные в формате ss://...$")
