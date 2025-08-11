from aiogram import types
from aiogram.types import ParseMode
import datetime
import logging

from data.config import OWNER, BOT_NAME, BOT_DESCRIPTION
from loader import bot, dp
from keyboards.inline import get_main_keyboard, get_admin_keyboard

logger = logging.getLogger(__name__)


@dp.message_handler(commands=['start'], chat_type='private')
async def start_cmd_message(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    logger.info(f"User {user_id} (@{username}) started the bot")
    
    # Приветственное сообщение
    welcome_text = f"""
<b>👋 Привет, {first_name}!</b>

Добро пожаловать в <b>{BOT_NAME}</b>

{BOT_DESCRIPTION}

Выберите действие из меню ниже:
"""
    
    # Проверяем, является ли пользователь администратором
    if user_id in OWNER:
        # Админская панель
        admin_text = f"""
<b>🔧 Панель администратора</b>

Добро пожаловать, <code>@{username}</code> (<code>{user_id}</code>)

Выберите действие:
"""
        await message.answer(
            admin_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_admin_keyboard()
        )
    else:
        # Обычное меню для пользователей
        await message.answer(
            welcome_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )


@dp.message_handler(commands=['menu'], chat_type='private')
async def menu_cmd_message(message: types.Message):
    """Обработчик команды /menu - показывает главное меню"""
    user_id = message.from_user.id
    
    if user_id in OWNER:
        await message.answer(
            "🔧 <b>Панель администратора</b>\n\nВыберите действие:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            "🏠 <b>Главное меню</b>\n\nВыберите действие:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )


@dp.message_handler(commands=['about'], chat_type='private')
async def about_cmd_message(message: types.Message):
    """Обработчик команды /about - информация о боте"""
    about_text = f"""
<b>ℹ️ О боте</b>

<b>Название:</b> {BOT_NAME}
<b>Описание:</b> {BOT_DESCRIPTION}
<b>Версия:</b> 1.0.0
<b>Фреймворк:</b> aiogram 2.x

Этот бот создан на основе шаблона aiogram 2.x
"""
    
    await message.answer(
        about_text,
        parse_mode=ParseMode.HTML
    )
