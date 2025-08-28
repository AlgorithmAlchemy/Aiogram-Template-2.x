from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import config


class UserFilter(BoundFilter):
    """Фильтр для проверки обычного пользователя"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, является ли пользователь обычным пользователем"""
        return message.from_user.id not in config.admin.owner_ids


class PrivateChatFilter(BoundFilter):
    """Фильтр для приватных чатов"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, что сообщение из приватного чата"""
        return message.chat.type == 'private'


class GroupChatFilter(BoundFilter):
    """Фильтр для групповых чатов"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, что сообщение из группового чата"""
        return message.chat.type in ['group', 'supergroup']


class SuperGroupFilter(BoundFilter):
    """Фильтр для супергрупп"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, что сообщение из супергруппы"""
        return message.chat.type == 'supergroup'


class HasUsernameFilter(BoundFilter):
    """Фильтр для пользователей с username"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, есть ли у пользователя username"""
        return bool(message.from_user.username)


class NoUsernameFilter(BoundFilter):
    """Фильтр для пользователей без username"""

    async def check(self, message: types.Message) -> bool:
        """Проверяет, нет ли у пользователя username"""
        return not bool(message.from_user.username)
