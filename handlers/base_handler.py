from abc import ABC, abstractmethod
from typing import List
from aiogram import types
from aiogram.dispatcher import Dispatcher
import logging

logger = logging.getLogger(__name__)


class BaseCommandHandler(ABC):
    """Базовый класс для обработчиков команд"""

    def __init__(self, dp: Dispatcher) -> None:
        self.dp: Dispatcher = dp
        self.register_handlers()

    @abstractmethod
    def get_command(self) -> str:
        """Возвращает команду для обработки"""
        pass

    @abstractmethod
    async def handle(self, message: types.Message) -> None:
        """Основной метод обработки команды"""
        pass

    def register_handlers(self) -> None:
        """Регистрирует обработчики команд"""
        self.dp.register_message_handler(
            self.handle,
            commands=[self.get_command()],
            chat_type='private'
        )
        logger.info(f"Registered handler for command: {self.get_command()}")


class BaseMessageHandler(ABC):
    """Базовый класс для обработчиков сообщений"""

    def __init__(self, dp: Dispatcher) -> None:
        self.dp: Dispatcher = dp
        self.register_handlers()

    @abstractmethod
    def get_content_types(self) -> List[str]:
        """Возвращает типы контента для обработки"""
        pass

    @abstractmethod
    async def handle(self, message: types.Message) -> None:
        """Основной метод обработки сообщения"""
        pass

    def register_handlers(self) -> None:
        """Регистрирует обработчики сообщений"""
        self.dp.register_message_handler(
            self.handle,
            content_types=self.get_content_types()
        )
        content_types = self.get_content_types()
        logger.info(
            f"Registered message handler for content types: {content_types}"
        )


class BaseCallbackHandler(ABC):
    """Базовый класс для обработчиков callback запросов"""

    def __init__(self, dp: Dispatcher) -> None:
        self.dp: Dispatcher = dp
        self.register_handlers()

    @abstractmethod
    def get_callback_data(self) -> str:
        """Возвращает callback_data для обработки"""
        pass

    @abstractmethod
    async def handle(self, callback_query: types.CallbackQuery) -> None:
        """Основной метод обработки callback"""
        pass

    def register_handlers(self) -> None:
        """Регистрирует обработчики callback"""
        self.dp.register_callback_query_handler(
            self.handle,
            lambda c: c.data == self.get_callback_data()
        )
        callback_data = self.get_callback_data()
        logger.info(f"Registered callback handler for data: {callback_data}")
