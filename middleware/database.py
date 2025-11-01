import logging
from typing import Any, Dict

from aiogram.types import Message, CallbackQuery

from middleware.base import BaseCustomMiddleware
from models.user import User

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseCustomMiddleware):
    async def pre_process(self, event: Message | CallbackQuery, data: Dict[str, Any]):
        """Preprocessing with a database"""
        user_id = event.from_user.id

        try:
            user = User.get_or_none(User.user_id == user_id)
            data['db_user'] = user

            if user:
                user.update_activity()
                logger.debug(f"User activity updated: {user_id}")

        except Exception as e:
            logger.error(f"Database error in middleware: {e}")
            data['db_user'] = None

    async def post_process(self, event: Message | CallbackQuery, data: Dict[str, Any], result: Any):

        pass
