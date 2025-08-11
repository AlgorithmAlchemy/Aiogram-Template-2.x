from aiogram import types
from aiogram.types import ParseMode
import logging
from datetime import datetime

from data.config import config
from loader import dp
from keyboards.inline.keyboards import MainKeyboards
from models.user import User, UserSettings, UserStats

logger = logging.getLogger(__name__)


class StartCommand:
    """Обработчик команды /start"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /start"""
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        
        logger.info(f"User {user_id} (@{username}) started the bot")
        
        # Создаем или обновляем пользователя в БД
        await StartCommand._create_or_update_user(message.from_user)
        
        # Приветственное сообщение
        welcome_text = StartCommand._get_welcome_text(first_name)
        
        # Проверяем, является ли пользователь администратором
        if user_id in config.admin.owner_ids:
            # Админская панель
            admin_text = StartCommand._get_admin_text(username, user_id)
            await message.answer(
                admin_text,
                parse_mode=ParseMode.HTML,
                reply_markup=MainKeyboards.get_admin_keyboard()
            )
        else:
            # Обычное меню для пользователей
            await message.answer(
                welcome_text,
                parse_mode=ParseMode.HTML,
                reply_markup=MainKeyboards.get_main_keyboard()
            )
    
    @staticmethod
    async def _create_or_update_user(user: types.User):
        """Создает или обновляет пользователя в базе данных"""
        try:
            # Проверяем, существует ли пользователь
            db_user = User.get_or_none(User.user_id == user.id)
            
            if db_user:
                # Обновляем существующего пользователя
                db_user.username = user.username
                db_user.first_name = user.first_name
                db_user.last_name = user.last_name
                db_user.updated_at = datetime.now()
                db_user.save()
                logger.info(f"Updated user {user.id} in database")
            else:
                # Создаем нового пользователя
                db_user = User.create(
                    user_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Создаем настройки пользователя
                UserSettings.create(user=db_user)
                
                # Создаем статистику пользователя
                UserStats.create(user=db_user)
                
                logger.info(f"Created new user {user.id} in database")
                
        except Exception as e:
            logger.error(f"Error creating/updating user {user.id}: {e}")
    
    @staticmethod
    def _get_welcome_text(first_name: str) -> str:
        """Генерирует приветственный текст"""
        return f"""
🎉 <b>Добро пожаловать, {first_name}!</b>

Я - {config.bot.name}, ваш персональный помощник.

<b>Что я умею:</b>
• Помогать с различными задачами
• Предоставлять полезную информацию
• Отвечать на ваши вопросы
• И многое другое!

<b>Поддержка:</b> {config.bot.support}

Используйте /help для получения справки или /menu для главного меню.
"""
    
    @staticmethod
    def _get_admin_text(username: str, user_id: int) -> str:
        """Генерирует текст для администратора"""
        return f"""
👑 <b>Панель администратора</b>

Добро пожаловать, {username}!

<b>Ваш ID:</b> <code>{user_id}</code>
<b>Роль:</b> Администратор

<b>Доступные действия:</b>
• Управление пользователями
• Просмотр статистики
• Настройка бота
• Модерация

Используйте кнопки ниже для навигации.
"""


# Регистрация обработчика
@dp.message_handler(commands=['start'], chat_type='private')
async def start_cmd(message: types.Message):
    await StartCommand.handle(message)
