from aiogram import types
from aiogram.types import ParseMode
import logging

from loader import dp
from models.user import User, UserStats

logger = logging.getLogger(__name__)


class EchoHandler:
    """Обработчик эхо-сообщений"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик всех текстовых сообщений"""
        user = message.from_user
        
        try:
            # Проверяем, забанен ли пользователь
            db_user = User.get_or_none(User.user_id == user.id)
            if db_user and db_user.is_banned:
                await message.answer("🚫 Вы заблокированы в боте.")
                return
            
            # Обновляем статистику сообщений
            if db_user:
                stats = UserStats.get_or_none(UserStats.user == db_user)
                if stats:
                    stats.increment_messages()
            
            # Простой эхо-ответ
            await message.answer(
                f"💬 <b>Эхо:</b> {message.text}",
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error in echo handler: {e}")
            await message.answer("❌ Произошла ошибка при обработке сообщения")


# Регистрация обработчика
@dp.message_handler(content_types=['text'], chat_type='private')
async def echo_handler(message: types.Message):
    await EchoHandler.handle(message)
