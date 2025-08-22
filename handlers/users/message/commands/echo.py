from aiogram import types
from aiogram.types import ParseMode
import logging

from loader import dp
from models.user import User, UserStats
from handlers.base_handler import BaseMessageHandler

logger = logging.getLogger(__name__)


class EchoMessageHandler(BaseMessageHandler):
    """Обработчик эхо-сообщений"""
    
    def get_content_types(self) -> list:
        return ['text']
    
    async def handle(self, message: types.Message):
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
                else:
                    # Создаем статистику, если её нет
                    stats = UserStats.create(user=db_user)
                    stats.increment_messages()
                
                # Обновляем время последней активности
                db_user.update_activity()
            
            # Простой эхо-ответ
            await message.answer(
                f"💬 <b>Эхо:</b> {message.text}",
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error in echo handler: {e}")
            await message.answer("❌ Произошла ошибка при обработке сообщения")


# Создаем экземпляр хэндлера для автоматической регистрации
echo_handler = EchoMessageHandler(dp)
