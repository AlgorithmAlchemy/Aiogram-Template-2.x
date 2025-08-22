"""
Базовые классы для middleware
"""
import logging
import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


class BaseCustomMiddleware(BaseMiddleware):
    """Базовый класс для всех middleware"""
    
    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Базовый метод вызова middleware"""
        start_time = time.time()
        
        try:
            # Предобработка
            await self.pre_process(event, data)
            
            # Выполнение обработчика
            result = await handler(event, data)
            
            # Постобработка
            await self.post_process(event, data, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            raise
        finally:
            # Логирование времени выполнения
            execution_time = time.time() - start_time
            if execution_time > 1.0:  # Логируем медленные запросы
                logger.warning(f"Slow request in {self.name}: {execution_time:.2f}s")
    
    async def pre_process(self, event: Message | CallbackQuery, data: Dict[str, Any]):
        """Предобработка события"""
        pass
    
    async def post_process(self, event: Message | CallbackQuery, data: Dict[str, Any], result: Any):
        """Постобработка события"""
        pass
