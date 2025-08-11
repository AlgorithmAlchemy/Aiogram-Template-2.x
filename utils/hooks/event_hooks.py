import logging
from typing import Callable, Any
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


class EventHooks:
    """Класс для управления хуками событий"""
    
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.hooks = {
            'on_startup': [],
            'on_shutdown': [],
            'on_message': [],
            'on_callback': [],
            'on_error': []
        }
    
    def register_startup_hook(self, func: Callable) -> None:
        """Зарегистрировать хук запуска"""
        self.hooks['on_startup'].append(func)
        logger.info(f"Registered startup hook: {func.__name__}")
    
    def register_shutdown_hook(self, func: Callable) -> None:
        """Зарегистрировать хук завершения"""
        self.hooks['on_shutdown'].append(func)
        logger.info(f"Registered shutdown hook: {func.__name__}")
    
    def register_message_hook(self, func: Callable) -> None:
        """Зарегистрировать хук сообщений"""
        self.hooks['on_message'].append(func)
        logger.info(f"Registered message hook: {func.__name__}")
    
    def register_callback_hook(self, func: Callable) -> None:
        """Зарегистрировать хук callback'ов"""
        self.hooks['on_callback'].append(func)
        logger.info(f"Registered callback hook: {func.__name__}")
    
    def register_error_hook(self, func: Callable) -> None:
        """Зарегистрировать хук ошибок"""
        self.hooks['on_error'].append(func)
        logger.info(f"Registered error hook: {func.__name__}")
    
    async def execute_startup_hooks(self) -> None:
        """Выполнить все хуки запуска"""
        for hook in self.hooks['on_startup']:
            try:
                await hook()
                logger.info(f"Executed startup hook: {hook.__name__}")
            except Exception as e:
                logger.error(f"Error in startup hook {hook.__name__}: {e}")
    
    async def execute_shutdown_hooks(self) -> None:
        """Выполнить все хуки завершения"""
        for hook in self.hooks['on_shutdown']:
            try:
                await hook()
                logger.info(f"Executed shutdown hook: {hook.__name__}")
            except Exception as e:
                logger.error(f"Error in shutdown hook {hook.__name__}: {e}")
    
    async def execute_message_hooks(self, message: Message) -> None:
        """Выполнить все хуки сообщений"""
        for hook in self.hooks['on_message']:
            try:
                await hook(message)
            except Exception as e:
                logger.error(f"Error in message hook {hook.__name__}: {e}")
    
    async def execute_callback_hooks(self, callback: CallbackQuery) -> None:
        """Выполнить все хуки callback'ов"""
        for hook in self.hooks['on_callback']:
            try:
                await hook(callback)
            except Exception as e:
                logger.error(f"Error in callback hook {hook.__name__}: {e}")
    
    async def execute_error_hooks(self, error: Exception, update: Any) -> None:
        """Выполнить все хуки ошибок"""
        for hook in self.hooks['on_error']:
            try:
                await hook(error, update)
            except Exception as e:
                logger.error(f"Error in error hook {hook.__name__}: {e}")


# Примеры хуков
async def startup_database_hook():
    """Хук для инициализации базы данных"""
    logger.info("Initializing database connection...")
    # Здесь можно добавить логику инициализации БД


async def shutdown_database_hook():
    """Хук для закрытия соединения с базой данных"""
    logger.info("Closing database connection...")
    # Здесь можно добавить логику закрытия БД


async def message_logging_hook(message: Message):
    """Хук для логирования сообщений"""
    logger.info(f"Message from {message.from_user.id}: {message.text}")


async def callback_logging_hook(callback: CallbackQuery):
    """Хук для логирования callback'ов"""
    logger.info(f"Callback from {callback.from_user.id}: {callback.data}")


async def error_logging_hook(error: Exception, update: Any):
    """Хук для логирования ошибок"""
    logger.error(f"Error occurred: {error} in update: {update}")


# Функция для настройки хуков
def setup_hooks(dp: Dispatcher) -> EventHooks:
    """Настроить все хуки"""
    hooks = EventHooks(dp)
    
    # Регистрируем стандартные хуки
    hooks.register_startup_hook(startup_database_hook)
    hooks.register_shutdown_hook(shutdown_database_hook)
    hooks.register_message_hook(message_logging_hook)
    hooks.register_callback_hook(callback_logging_hook)
    hooks.register_error_hook(error_logging_hook)
    
    return hooks
