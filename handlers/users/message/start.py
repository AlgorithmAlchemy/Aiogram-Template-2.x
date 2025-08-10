from aiogram import types
import datetime
import asyncio

from aiogram.utils import exceptions
import re
from data.config import OWNER
from loader import bot, dp
import aiogram.utils

# Создаем словарь для отслеживания предыдущих сообщений пользователя
user_messages = {}

import asyncio
import re

from aiogram import types
from aiogram.utils import exceptions

from data.config import OWNER
from loader import bot, dp

# Создаем словарь для отслеживания предыдущих сообщений пользователя
user_messages = {}


@dp.message_handler(commands=['start'], chat_type='private')
async def start_cmd_message(message: types.Message):
    if message.from_user.id in OWNER:
        await message.delete()
        with open("data/message_urls") as openfile:
            lines = openfile.readlines()

        pattern = re.compile(re.escape(str(message.from_user.id)))
        with open('data/message_urls', 'w') as f:
            for line in lines:
                result = pattern.search(line)
                if result is None:
                    f.write(line)

        for line in lines:
            if f'{message.from_user.id}' in line:
                txt_message_id = int(line.replace('\n', '').replace(" ", "").split(",")[1])
                try:
                    await bot.delete_message(chat_id=message.from_user.id, message_id=txt_message_id)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                except aiogram.utils.exceptions.MessageCantBeDeleted:
                    pass

        # Отправляем новое сообщение
        mes = await message.answer(f'Welcome to admin panel <code>@{message.from_user.username}</code>'
                                   f'(<code>{message.from_user.id}</code>)'
                                   f'\nВоспользуйтесь клавиатурой для генерации.', reply_markup=
        pass)

        # Запоминаем ID нового сообщения
        user_messages[message.from_user.id] = mes.message_id

        txt_export = open("data/message_urls", 'a+')

        txt_export.write(
            f"{str(message.chat.id)}, {str(message.message_id)}\n")

        button_mess_ids = int(message.message_id)
        button_mess_ids += 1
        txt_export.write(
            f"{str(message.chat.id)}, {str(button_mess_ids)}\n")

        txt_export.close()
