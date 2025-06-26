from aiogram import types

from data import config
from loader import dp, bot


@dp.message_handler(commands=['help'], chat_type='private')
async def start_cmd_message(message: types.Message):
    chat_id = message.chat.id
    send_status = 0
    for i in config.OWNER:
        if int(i) == int(chat_id):
            send_status += 1
            await bot.send_message(chat_id, config.admin_help_ru, parse_mode='HTML')

    if send_status == 0:
        await bot.send_message(chat_id, config.help_rus)