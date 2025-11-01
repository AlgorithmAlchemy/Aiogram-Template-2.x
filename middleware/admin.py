import logging
from typing import Any, Dict

from aiogram.types import Message, CallbackQuery

from data.config import config
from middleware.base import BaseCustomMiddleware

logger = logging.getLogger(__name__)


class AdminMiddleware(BaseCustomMiddleware):
    async def pre_process(self, event: Message | CallbackQuery, data: Dict[str, Any]):
        """Verification of administrator privileges"""
        user_id = event.from_user.id

        # Check if the user is an administrator
        is_admin = user_id in config.admin.owner_ids
        data['is_admin'] = is_admin

        # Logging admin access
        if is_admin:
            logger.debug(f"Admin access: {user_id}")
