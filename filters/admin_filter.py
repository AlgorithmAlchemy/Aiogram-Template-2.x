from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import config


class AdminFilter(BoundFilter):
    """Фильтр для проверки администратора"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, является ли пользователь администратором"""
        return message.from_user.id in config.admin.owner_ids


class SuperAdminFilter(BoundFilter):
    """Фильтр для проверки суперадминистратора (первый в списке)"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, является ли пользователь суперадминистратором"""
        if not config.admin.owner_ids:
            return False
        return message.from_user.id == config.admin.owner_ids[0]


class AdminOrOwnerFilter(BoundFilter):
    """Фильтр для проверки администратора или владельца чата"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет права администратора или владельца чата"""
        # Проверка на администратора бота
        if message.from_user.id in config.admin.owner_ids:
            return True

        # Проверка на владельца чата (для групп)
        if message.chat.type in ['group', 'supergroup']:
            chat_member = await message.bot.get_chat_member(
                message.chat.id, message.from_user.id
            )
            return chat_member.status in ['creator', 'administrator']

        return False
