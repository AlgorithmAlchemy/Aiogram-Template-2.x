"""
Главный файл бота
"""
import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import AllowedUpdates
from aiogram.utils import executor

from data.config import config
from loader import dp, bot
from models.sqlite3_creator import connect as db_connect
from utils.misc.logging import setup_logging

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)


class BotManager:
    """Менеджер бота для управления жизненным циклом"""
    
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.start_time = None
    
    async def on_startup(self, dp: Dispatcher):
        """Действия при запуске бота"""
        self.start_time = datetime.now()
        logger.info("Bot starting up...")
        
        try:
            # Подключение к базе данных
            db_connect()
            logger.info("Database connected successfully")
            
            # Регистрация хэндлеров
            await self.register_handlers()
            logger.info("Handlers registered successfully")
            
            # Регистрация middleware
            await self.setup_middleware()
            logger.info("Middleware setup completed")
            
            # Регистрация фильтров
            await self.setup_filters()
            logger.info("Filters setup completed")
            
            # Регистрация ошибок
            await self.setup_error_handlers()
            logger.info("Error handlers setup completed")
            
            logger.info(f"Bot started successfully at {self.start_time}")
            
        except Exception as e:
            logger.error(f"Error during startup: {e}")
            raise
    
    async def on_shutdown(self, dp: Dispatcher):
        """Действия при остановке бота"""
        logger.info("Bot shutting down...")
        
        try:
            # Закрытие соединений
            await self.bot.session.close()
            logger.info("Bot session closed")
            
            # Дополнительная очистка если нужно
            logger.info(f"Bot stopped. Uptime: {datetime.now() - self.start_time}")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    async def register_handlers(self):
        """Регистрация всех хэндлеров"""
        
        # Импортируем хэндлеры команд
        from handlers.users.message.commands.start import StartCommandHandler
        from handlers.users.message.commands.profile import ProfileCommandHandler
        from handlers.users.message.commands.help import HelpCommandHandler
        from handlers.users.message.commands.about import AboutCommandHandler
        from handlers.users.message.commands.settings import SettingsCommandHandler
        from handlers.users.message.commands.stats import StatsCommandHandler
        from handlers.users.message.commands.users import UsersCommandHandler
        from handlers.users.message.commands.status import StatusCommandHandler
        from handlers.users.message.commands.version import VersionCommandHandler
        from handlers.users.message.commands.uptime import UptimeCommandHandler
        from handlers.users.message.commands.commands import CommandsCommandHandler
        from handlers.users.message.commands.menu import MenuCommandHandler
        from handlers.users.message.commands.ping import PingCommandHandler
        from handlers.users.message.commands.feedback import FeedbackCommandHandler
        from handlers.users.message.commands.support import SupportCommandHandler
        from handlers.users.message.commands.weather import WeatherCommandHandler
        
        # Импортируем хэндлеры модерации
        from handlers.users.message.commands.ban_user import BanUserCommandHandler
        from handlers.users.message.commands.unban_user import UnbanUserCommandHandler
        from handlers.users.message.commands.warn_user import WarnUserCommandHandler
        
        # Импортируем хэндлеры сообщений
        from handlers.users.message.commands.echo import EchoMessageHandler
        
        # Создаем экземпляры хэндлеров для автоматической регистрации
        handlers = [
            # Основные команды
            StartCommandHandler(self.dp),
            ProfileCommandHandler(self.dp),
            HelpCommandHandler(self.dp),
            AboutCommandHandler(self.dp),
            SettingsCommandHandler(self.dp),
            StatusCommandHandler(self.dp),
            VersionCommandHandler(self.dp),
            UptimeCommandHandler(self.dp),
            CommandsCommandHandler(self.dp),
            MenuCommandHandler(self.dp),
            PingCommandHandler(self.dp),
            FeedbackCommandHandler(self.dp),
            SupportCommandHandler(self.dp),
            WeatherCommandHandler(self.dp),
            
            # Админские команды
            StatsCommandHandler(self.dp),
            UsersCommandHandler(self.dp),
            BanUserCommandHandler(self.dp),
            UnbanUserCommandHandler(self.dp),
            WarnUserCommandHandler(self.dp),
            
            # Обработчики сообщений
            EchoMessageHandler(self.dp),
        ]
        
        logger.info(f"Registered {len(handlers)} handlers")
    
    async def setup_middleware(self):
        """Настройка middleware"""
        try:
            from middleware.logging import LoggingMiddleware
            from middleware.throttling import ThrottlingMiddleware
            from middleware.admin import AdminMiddleware
            from middleware.database import DatabaseMiddleware
            
            # Базовое логирование
            self.dp.middleware.setup(LoggingMiddleware())
            
            # Throttling для защиты от спама
            if config.debug:
                self.dp.middleware.setup(ThrottlingMiddleware())
            
            # Проверка администраторов
            self.dp.middleware.setup(AdminMiddleware())
            
            # Работа с базой данных
            self.dp.middleware.setup(DatabaseMiddleware())
            
        except Exception as e:
            logger.error(f"Error setting up middleware: {e}")
    
    async def setup_filters(self):
        """Настройка фильтров"""
        try:
            from filters.admin_filter import AdminFilter
            from filters.user_filter import UserFilter
            
            # Регистрируем фильтры
            self.dp.filters_factory.bind(AdminFilter)
            self.dp.filters_factory.bind(UserFilter)
            
        except Exception as e:
            logger.error(f"Error setting up filters: {e}")
    
    async def setup_error_handlers(self):
        """Настройка обработчиков ошибок"""
        try:
            from handlers.errors.message import register_message_error_handlers
            from handlers.errors.callback import register_callback_error_handlers
            
            # Регистрируем обработчики ошибок
            register_message_error_handlers(self.dp)
            register_callback_error_handlers(self.dp)
            
        except Exception as e:
            logger.error(f"Error setting up error handlers: {e}")


# Создаем менеджер бота
bot_manager = BotManager(bot, dp)


def main():
    """Главная функция запуска бота"""
    logger.info("Starting bot...")
    
    # Запускаем бота
    executor.start_polling(
        dispatcher=dp,
        on_startup=bot_manager.on_startup,
        on_shutdown=bot_manager.on_shutdown,
        
        # ============================================
        # ALLOWED_UPDATES - актуальные методы для aiogram 2.x
        # ============================================
        #
        # 1. Все обновления (по умолчанию)
        allowed_updates=AllowedUpdates.all(),
        #
        # 2. Только сообщения
        # allowed_updates=AllowedUpdates.MESSAGE,
        #
        # 3. Только callback запросы
        # allowed_updates=AllowedUpdates.CALLBACK_QUERY,
        #
        # 4. Только inline запросы
        # allowed_updates=AllowedUpdates.INLINE_QUERY,
        #
        # 5. Только chosen inline результаты
        # allowed_updates=AllowedUpdates.CHOSEN_INLINE_RESULT,
        #
        # 6. Только channel posts
        # allowed_updates=AllowedUpdates.CHANNEL_POST,
        #
        # 7. Только edited channel posts
        # allowed_updates=AllowedUpdates.EDITED_CHANNEL_POST,
        #
        # 8. Только edited messages
        # allowed_updates=AllowedUpdates.EDITED_MESSAGE,
        #
        # 9. Только shipping queries
        # allowed_updates=AllowedUpdates.SHIPPING_QUERY,
        #
        # 10. Только pre-checkout queries
        # allowed_updates=AllowedUpdates.PRE_CHECKOUT_QUERY,
        #
        # 11. Только poll answers
        # allowed_updates=AllowedUpdates.POLL_ANSWER,
        #
        # 12. Только my chat member updates
        # allowed_updates=AllowedUpdates.MY_CHAT_MEMBER,
        #
        # 13. Только chat member updates
        # allowed_updates=AllowedUpdates.CHAT_MEMBER,
        #
        # 14. Только chat join requests
        # allowed_updates=AllowedUpdates.CHAT_JOIN_REQUEST,
        #
        # 15. Комбинация нескольких типов
        # allowed_updates=[
        #     AllowedUpdates.MESSAGE,
        #     AllowedUpdates.CALLBACK_QUERY,
        #     AllowedUpdates.EDITED_MESSAGE
        # ],
        #
        # 16. Только сообщения и callback запросы (оптимально для большинства ботов)
        # allowed_updates=[
        #     AllowedUpdates.MESSAGE,
        #     AllowedUpdates.CALLBACK_QUERY
        # ],
        #
        # 17. Только сообщения (для простых ботов)
        # allowed_updates=AllowedUpdates.MESSAGE,
        #
        # 18. Все кроме channel posts (для приватных ботов)
        # allowed_updates=[
        #     AllowedUpdates.MESSAGE,
        #     AllowedUpdates.EDITED_MESSAGE,
        #     AllowedUpdates.CALLBACK_QUERY,
        #     AllowedUpdates.INLINE_QUERY,
        #     AllowedUpdates.CHOSEN_INLINE_RESULT,
        #     AllowedUpdates.SHIPPING_QUERY,
        #     AllowedUpdates.PRE_CHECKOUT_QUERY,
        #     AllowedUpdates.POLL_ANSWER,
        #     AllowedUpdates.MY_CHAT_MEMBER,
        #     AllowedUpdates.CHAT_MEMBER,
        #     AllowedUpdates.CHAT_JOIN_REQUEST
        # ],
        
        # Дополнительные параметры
        skip_updates=True,  # Пропускаем старые обновления
        timeout=20,  # Таймаут для long polling
        relax=0.1,  # Задержка между запросами
    )


if __name__ == "__main__":
    main()
