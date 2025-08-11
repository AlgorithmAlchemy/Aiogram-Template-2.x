from aiogram import types
from aiogram.types import ParseMode

from data import config
from loader import dp, bot
from keyboards.inline.keyboards import get_back_keyboard

import logging

logger = logging.getLogger(__name__)


@dp.message_handler(commands=['help'], chat_type='private')
async def help_cmd_message(message: types.Message):
    """Обработчик команды /help"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    logger.info(f"User {user_id} requested help")
    
    # Проверяем, является ли пользователь администратором
    for admin_id in config.OWNER:
        if int(admin_id) == int(chat_id):
            # Админская справка
            await bot.send_message(
                chat_id, 
                config.admin_help_ru, 
                parse_mode=ParseMode.HTML
            )
            return
    
    # Обычная справка для пользователей
    await bot.send_message(
        chat_id, 
        config.help_rus,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


@dp.message_handler(commands=['commands'], chat_type='private')
async def commands_cmd_message(message: types.Message):
    """Обработчик команды /commands - показывает все доступные команды"""
    commands_text = """
<b>📋 Доступные команды</b>

<b>Основные команды:</b>
/start - Запустить бота и показать главное меню
/menu - Показать главное меню
/help - Показать справку
/about - Информация о боте
/commands - Показать все команды

<b>Пользовательские команды:</b>
/profile - Показать ваш профиль
/settings - Открыть настройки

<b>Админские команды:</b>
/stats - Статистика бота (только для админов)
/users - Список пользователей (только для админов)

<b>Поддержка:</b> {support}
""".format(support=config.SUPPORT)
    
    await message.answer(
        commands_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


@dp.message_handler(commands=['profile'], chat_type='private')
async def profile_cmd_message(message: types.Message):
    """Обработчик команды /profile - показывает профиль пользователя"""
    user = message.from_user
    
    profile_text = f"""
<b>📋 Профиль пользователя</b>

<b>ID:</b> <code>{user.id}</code>
<b>Имя:</b> {user.first_name}
<b>Фамилия:</b> {user.last_name or 'Не указана'}
<b>Username:</b> @{user.username or 'Не указан'}
<b>Дата регистрации:</b> {message.date.strftime('%d.%m.%Y %H:%M')}

<b>Статус:</b> {'👑 Администратор' if user.id in config.OWNER else '👤 Пользователь'}

<b>Информация о чате:</b>
<b>Тип чата:</b> {message.chat.type}
<b>ID чата:</b> <code>{message.chat.id}</code>
"""
    
    await message.answer(
        profile_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )
