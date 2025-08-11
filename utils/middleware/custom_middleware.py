import logging
import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from data.config import config

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования всех обновлений"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Логируем входящее обновление
        if isinstance(event, Message):
            logger.info(
                f"Message from {event.from_user.id} (@{event.from_user.username}): "
                f"{event.text[:50]}..."
            )
        elif isinstance(event, CallbackQuery):
            logger.info(
                f"Callback from {event.from_user.id} (@{event.from_user.username}): "
                f"{event.data}"
            )
        
        # Выполняем обработчик
        result = await handler(event, data)
        
        # Логируем результат
        logger.info(f"Handler completed successfully")
        
        return result


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware для ограничения частоты запросов"""
    
    def __init__(self, rate_limit: float = 0.5):
        super().__init__()
        self.rate_limit = rate_limit
        self.last_request = {}
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()
        
        # Проверяем ограничение частоты
        if user_id in self.last_request:
            time_passed = current_time - self.last_request[user_id]
            if time_passed < self.rate_limit:
                await event.answer("⚠️ Слишком много запросов. Подождите немного.")
                return
        
        # Обновляем время последнего запроса
        self.last_request[user_id] = current_time
        
        # Выполняем обработчик
        return await handler(event, data)


class AdminMiddleware(BaseMiddleware):
    """Middleware для проверки прав администратора"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        # Проверяем, является ли пользователь администратором
        is_admin = user_id in config.admin.owner_ids
        data['is_admin'] = is_admin
        
        # Выполняем обработчик
        return await handler(event, data)


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для работы с базой данных"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Здесь можно добавить логику для работы с БД
        # Например, создание/обновление пользователя
        
        # Выполняем обработчик
        result = await handler(event, data)
        
        # Здесь можно добавить логику после обработки
        # Например, сохранение статистики
        
        return result


class MetricsMiddleware(BaseMiddleware):
    """Middleware для сбора метрик"""
    
    def __init__(self):
        super().__init__()
        self.metrics = {
            'total_messages': 0,
            'total_callbacks': 0,
            'errors': 0
        }
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Увеличиваем счетчики
        if isinstance(event, Message):
            self.metrics['total_messages'] += 1
        elif isinstance(event, CallbackQuery):
            self.metrics['total_callbacks'] += 1
        
        try:
            # Выполняем обработчик
            result = await handler(event, data)
            return result
        except Exception as e:
            # Увеличиваем счетчик ошибок
            self.metrics['errors'] += 1
            logger.error(f"Error in handler: {e}")
            raise
    
    def get_metrics(self) -> Dict[str, int]:
        """Получить текущие метрики"""
        return self.metrics.copy()
