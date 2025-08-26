import logging
from aiogram import Dispatcher
from middleware.base import BaseCustomMiddleware
from middleware.logging import LoggingMiddleware
from middleware.throttling import ThrottlingMiddleware
from middleware.admin import AdminMiddleware
from middleware.database import DatabaseMiddleware

logger = logging.getLogger(__name__)


class CustomMiddleware(BaseCustomMiddleware):
    """Пример кастомного middleware"""
    
    async def pre_process(self, event, data):
        """Предобработка"""
        logger.info(f"Custom middleware pre-process: {event.from_user.id}")
        data['custom_data'] = "Hello from custom middleware!"
    
    async def post_process(self, event, data, result):
        """Постобработка"""
        logger.info(f"Custom middleware post-process: {event.from_user.id}")


def setup_middleware_example(dp: Dispatcher):
    """Пример настройки middleware"""
    
    # Базовое логирование
    dp.middleware.setup(LoggingMiddleware())
    
    # Ограничение частоты запросов
    dp.middleware.setup(ThrottlingMiddleware(rate_limit=1.0))
    
    # Проверка администраторов
    dp.middleware.setup(AdminMiddleware())
    
    # Работа с базой данных
    dp.middleware.setup(DatabaseMiddleware())
    
    # Кастомный middleware
    dp.middleware.setup(CustomMiddleware())
    
    logger.info("Middleware setup completed")


def middleware_usage_example():
    """Пример использования данных из middleware в хэндлере"""
    
    # В хэндлере можно получить данные из middleware:
    """
    @dp.message_handler(commands=['test'])
    async def test_handler(message: types.Message, data: dict):
        # Данные из AdminMiddleware
        is_admin = data.get('is_admin', False)
        
        # Данные из DatabaseMiddleware
        db_user = data.get('db_user')
        
        # Данные из CustomMiddleware
        custom_data = data.get('custom_data')
        
        await message.answer(f"Admin: {is_admin}, User: {db_user}, Custom: {custom_data}")
    """
    
    print("Middleware usage example:")
    print("- data['is_admin'] - права администратора")
    print("- data['db_user'] - пользователь из БД")
    print("- data['custom_data'] - кастомные данные")


def create_custom_middleware():
    """Пример создания кастомного middleware"""
    
    class UserStatsMiddleware(BaseCustomMiddleware):
        """Middleware для сбора статистики пользователей"""
        
        def __init__(self):
            super().__init__()
            self.stats = {}
        
        async def pre_process(self, event, data):
            user_id = event.from_user.id
            
            # Инициализируем статистику пользователя
            if user_id not in self.stats:
                self.stats[user_id] = {
                    'requests': 0,
                    'last_request': None
                }
            
            # Обновляем статистику
            self.stats[user_id]['requests'] += 1
            self.stats[user_id]['last_request'] = event.date
            
            # Добавляем в данные
            data['user_stats'] = self.stats[user_id]
        
        async def post_process(self, event, data, result):
            # Можно добавить постобработку
            pass
    
    return UserStatsMiddleware()


def main():
    """Демонстрация middleware"""
    print("=== Middleware Examples ===")
    
    # Пример настройки
    print("\n1. Setup example:")
    print("dp.middleware.setup(LoggingMiddleware())")
    print("dp.middleware.setup(ThrottlingMiddleware())")
    print("dp.middleware.setup(AdminMiddleware())")
    print("dp.middleware.setup(DatabaseMiddleware())")
    
    # Пример использования
    print("\n2. Usage in handlers:")
    middleware_usage_example()
    
    # Пример создания кастомного middleware
    print("\n3. Custom middleware:")
    custom_middleware = create_custom_middleware()
    print(f"Created: {custom_middleware.__class__.__name__}")
    
    print("\n=== Middleware Examples Completed ===")


if __name__ == "__main__":
    main()
