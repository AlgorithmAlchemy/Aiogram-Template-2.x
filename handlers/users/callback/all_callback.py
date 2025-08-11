import asyncio
import json
from datetime import date, timedelta
import sys
import logging

from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram import types, utils
from aiogram.types import Update

from loader import dp, bot
import sqlite3
from models.sqlite3_creator import db, connect

from datetime import datetime
from data.config import OWNER, SUPPORT
from keyboards.inline.keyboards import (
    get_main_keyboard, get_admin_keyboard, get_settings_keyboard,
    get_confirm_keyboard, get_back_keyboard
)

logger = logging.getLogger(__name__)


@dp.callback_query_handler(lambda c: c.data == "main_menu")
async def main_menu_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Главное меню'"""
    user_id = callback_query.from_user.id
    
    if user_id in OWNER:
        await callback_query.message.edit_text(
            "🔧 <b>Панель администратора</b>\n\nВыберите действие:",
            parse_mode=types.ParseMode.HTML,
            reply_markup=get_admin_keyboard()
        )
    else:
        await callback_query.message.edit_text(
            "🏠 <b>Главное меню</b>\n\nВыберите действие:",
            parse_mode=types.ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "profile")
async def profile_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Профиль'"""
    user = callback_query.from_user
    
    profile_text = f"""
<b>📋 Профиль пользователя</b>

<b>ID:</b> <code>{user.id}</code>
<b>Имя:</b> {user.first_name}
<b>Фамилия:</b> {user.last_name or 'Не указана'}
<b>Username:</b> @{user.username or 'Не указан'}
<b>Дата регистрации:</b> {datetime.now().strftime('%d.%m.%Y')}

<b>Статус:</b> {'👑 Администратор' if user.id in OWNER else '👤 Пользователь'}
"""
    
    await callback_query.message.edit_text(
        profile_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "settings")
async def settings_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Настройки'"""
    settings_text = """
<b>⚙️ Настройки</b>

Здесь вы можете настроить параметры бота под свои предпочтения.

Выберите категорию настроек:
"""
    
    await callback_query.message.edit_text(
        settings_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_settings_keyboard()
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "help")
async def help_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Помощь'"""
    help_text = """
<b>❓ Помощь</b>

<b>Основные команды:</b>
/start - Запустить бота
/menu - Главное меню
/help - Показать эту справку
/about - Информация о боте

<b>Дополнительные команды:</b>
/profile - Ваш профиль
/settings - Настройки

<b>Поддержка:</b> {support}
""".format(support=SUPPORT)
    
    await callback_query.message.edit_text(
        help_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "about")
async def about_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'О боте'"""
    about_text = """
<b>ℹ️ О боте</b>

Этот бот создан на основе шаблона aiogram 2.x

<b>Возможности:</b>
• Удобное меню с кнопками
• Система администраторов
• Настройки пользователей
• Профили пользователей

<b>Технологии:</b>
• Python 3.10+
• aiogram 2.x
• SQLite база данных
• APScheduler для задач

<b>Разработчик:</b> Создано на основе шаблона
"""
    
    await callback_query.message.edit_text(
        about_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "support")
async def support_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Поддержка'"""
    support_text = f"""
<b>🔗 Поддержка</b>

Если у вас есть вопросы или проблемы, обратитесь к нам:

<b>Поддержка:</b> {SUPPORT}

<b>Время работы:</b> 24/7

<b>Что можно спросить:</b>
• Как использовать бота
• Сообщить об ошибке
• Предложить улучшения
• Техническая поддержка
"""
    
    await callback_query.message.edit_text(
        support_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()


# Админские callback обработчики
@dp.callback_query_handler(lambda c: c.data == "admin_stats")
async def admin_stats_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Статистика' для админов"""
    if callback_query.from_user.id not in OWNER:
        await callback_query.answer("❌ У вас нет прав администратора!", show_alert=True)
        return
    
    stats_text = """
<b>📊 Статистика бота</b>

<b>Общая статистика:</b>
• Пользователей: 0
• Сообщений: 0
• Команд: 0

<b>За сегодня:</b>
• Новых пользователей: 0
• Активных пользователей: 0

<b>Система:</b>
• Время работы: 0 дней
• Версия: 1.0.0
"""
    
    await callback_query.message.edit_text(
        stats_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard("main_menu")
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "admin_users")
async def admin_users_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Пользователи' для админов"""
    if callback_query.from_user.id not in OWNER:
        await callback_query.answer("❌ У вас нет прав администратора!", show_alert=True)
        return
    
    users_text = """
<b>👥 Пользователи</b>

Функция в разработке.

Здесь будет список пользователей бота с возможностью управления.
"""
    
    await callback_query.message.edit_text(
        users_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard("main_menu")
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "admin_ban")
async def admin_ban_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Бан пользователя' для админов"""
    if callback_query.from_user.id not in OWNER:
        await callback_query.answer("❌ У вас нет прав администратора!", show_alert=True)
        return
    
    ban_text = """
<b>🚫 Бан пользователя</b>

Функция в разработке.

Здесь будет возможность забанить пользователя по ID или username.
"""
    
    await callback_query.message.edit_text(
        ban_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=get_back_keyboard("main_menu")
    )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == "cancel")
async def cancel_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Отмена'"""
    await callback_query.message.delete()
    await callback_query.answer("❌ Действие отменено")
