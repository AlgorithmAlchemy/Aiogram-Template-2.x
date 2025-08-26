import time
import logging
from typing import Any, Dict
from aiogram.types import Message, CallbackQuery

from middleware.base import BaseCustomMiddleware

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseCustomMiddleware):
    """Middleware для ограничения частоты запросов"""
    
    def __init__(self, rate_limit: float = 0.5):
        super().__init__()
        self.rate_limit = rate_limit
        self.last_request = {}
    
    async def pre_process(self, event: Message | CallbackQuery, data: Dict[str, Any]):
        """Проверка ограничения частоты"""
        user_id = event.from_user.id
        current_time = time.time()
        
        # Проверяем ограничение частоты
        if user_id in self.last_request:
            time_passed = current_time - self.last_request[user_id]
            if time_passed < self.rate_limit:
                if isinstance(event, Message):
                    await event.answer(
                        "⚠️ Слишком много запросов. Подождите немного."
                    )
                elif isinstance(event, CallbackQuery):
                    await event.answer(
                        "⚠️ Слишком много запросов. Подождите немного.",
                        show_alert=True
                    )
                raise Exception("Rate limit exceeded")
        
        # Обновляем время последнего запроса
        self.last_request[user_id] = current_time
