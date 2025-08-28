from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, bot


class AdminWriteUserBan(StatesGroup):
    admin_write_user_ban = State()


@dp.message_handler(regexp=r'ban_user')
async def about_bot_message(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, '<b>Напиши юзернейм или айди пользователя</b>',
                           parse_mode='HTML', reply_markup=cancel_admin())

    await AdminWriteUserBan.admin_write_user_ban.set()


@dp.message_handler(state=AdminWriteUserBan.admin_write_user_ban, chat_type='private')
async def admin_write_username_id_ban(msg: types.Message, state: FSMContext):
    if msg.text.startswith('@'):
        usernames = msg.text.replace('@', '')
        if User.get_or_none(User.username == usernames):
            await bot.send_message(msg.from_user.id, '<b>Пользователь забанен!</b>', parse_mode='HTML')
            user = User.get(username=usernames)
            user.is_ban = 1
            user.save()
            await state.finish()
        else:
            await bot.send_message(msg.from_user.id, '<b>❌Такого пользователя нет</b>', parse_mode='HTML')
            await state.finish()
    else:
        try:
            user_id = int(msg.text)
            if User.get_or_none(User.id == user_id):
                await bot.send_message(msg.from_user.id, '<b>Пользователь забанен!</b>', parse_mode='HTML')
                user = User.get(User.id == user_id)
                user.is_ban = 1
                user.save()
                await state.finish()
            else:
                await bot.send_message(msg.from_user.id, '<b>❌Такого пользователя нет</b>', parse_mode='HTML')
                await state.finish()
        except:
            await bot.send_message(msg.from_user.id, '<b>❗️Пожалуйста, введи id пользователя или его username</b>',
                                   parse_mode='HTML')
            return
