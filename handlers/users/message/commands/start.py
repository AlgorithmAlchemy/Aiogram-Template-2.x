import logging
from datetime import datetime

from aiogram import types
from aiogram.types import ParseMode

from data.config import config
from handlers.base_handler import BaseCommandHandler
from keyboards.inline.keyboards import MainKeyboards
from loader import dp
from models.user import User, UserSettings, UserStats

logger = logging.getLogger(__name__)


class StartCommandHandler(BaseCommandHandler):
    """Обработчик команды /start"""

    def get_command(self) -> str:
        return "start"

    async def handle(self, message: types.Message):
        """Обработчик команды /start"""
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name

        logger.info(f"User {user_id} (@{username}) started the bot")

        # Создаем или обновляем пользователя в БД
        await self._create_or_update_user(message.from_user)

        # Приветственное сообщение
        welcome_text = self._get_welcome_text(first_name)

        # Проверяем, является ли пользователь администратором
        if user_id in config.admin.owner_ids:
            # Админская панель
            admin_text = self._get_admin_text(username, user_id)
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

    async def _create_or_update_user(self, user: types.User):
        """Создает или обновляет пользователя в базе данных"""
        try:
            # Проверяем, существует ли пользователь
            db_user = User.get_or_none(User.user_id == user.id)

            if db_user:
                # Обновляем существующего пользователя
                db_user.username = user.username
                db_user.first_name = user.first_name
                db_user.last_name = user.last_name
                db_user.language_code = user.language_code
                db_user.updated_at = datetime.now()
                db_user.last_activity = datetime.now()
                db_user.save()
                logger.info(f"Updated user {user.id} in database")
            else:
                # Создаем нового пользователя
                db_user = User.create(
                    user_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    language_code=user.language_code,
                    is_bot=user.is_bot,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    last_activity=datetime.now()
                )

                # Создаем настройки пользователя
                UserSettings.create(user=db_user)

                # Создаем статистику пользователя
                UserStats.create(user=db_user)

                logger.info(f"Created new user {user.id} in database")

        except Exception as e:
            logger.error(f"Error creating/updating user {user.id}: {e}")

    def _get_welcome_text(self, first_name: str) -> str:
        """Генерирует приветственный текст"""
        return f"""
<b>👋 Привет, {first_name}!</b>

Добро пожаловать в бота! 🤖

<b>Доступные команды:</b>
• /start - Главное меню
• /help - Справка
• /profile - Ваш профиль
• /settings - Настройки
• /about - О боте

<b>Поддержка:</b> @support_username

<i>Используйте кнопки ниже для навигации</i>
"""

    def _get_admin_text(self, username: str, user_id: int) -> str:
        """Генерирует текст для администратора"""
        return f"""
<b>👑 Панель администратора</b>

<b>Добро пожаловать, {username}!</b>

<b>Ваш ID:</b> <code>{user_id}</code>

<b>Админские команды:</b>
• /ban_user - Забанить пользователя
• /unban_user - Разбанить пользователя
• /warn_user - Предупредить пользователя
• /stats - Статистика бота
• /users - Список пользователей
• /broadcast - Отправить сообщение всем

<b>Обычные команды:</b>
• /profile - Ваш профиль
• /settings - Настройки
• /help - Справка

<i>Используйте кнопки ниже для управления</i>
"""


# Создаем экземпляр хэндлера для автоматической регистрации
start_handler = StartCommandHandler(dp)
