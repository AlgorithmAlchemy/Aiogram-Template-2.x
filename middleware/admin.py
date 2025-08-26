import logging
from typing import Any, Dict
from aiogram.types import Message, CallbackQuery

from middleware.base import BaseCustomMiddleware
from data.config import config

logger = logging.getLogger(__name__)


class AdminMiddleware(BaseCustomMiddleware):
    """Middleware для проверки прав администратора"""
    
    async def pre_process(self, event: Message | CallbackQuery, data: Dict[str, Any]):
        """Проверка прав администратора"""
        user_id = event.from_user.id
        
        # Проверяем, является ли пользователь администратором
        is_admin = user_id in config.admin.owner_ids
        data['is_admin'] = is_admin
        
        # Логируем доступ администратора
        if is_admin:
            logger.debug(f"Admin access: {user_id}")
