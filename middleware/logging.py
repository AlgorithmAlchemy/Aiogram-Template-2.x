import logging
from typing import Any, Dict

from aiogram.types import Message, CallbackQuery

from middleware.base import BaseCustomMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseCustomMiddleware):
    """Middleware для логирования всех обновлений"""

    async def pre_process(self, event: Message | CallbackQuery, data: Dict[str, Any]):
        """Логирование входящего обновления"""
        user = event.from_user

        if isinstance(event, Message):
            logger.info(
                f"Message from {user.id} (@{user.username}): "
                f"{event.text[:50] if event.text else 'No text'}..."
            )
        elif isinstance(event, CallbackQuery):
            logger.info(
                f"Callback from {user.id} (@{user.username}): "
                f"{event.data}"
            )

    async def post_process(self, event: Message | CallbackQuery, data: Dict[str, Any], result: Any):
        """Логирование результата"""
        logger.info(f"Handler completed successfully for {self.name}")
