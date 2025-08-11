from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.contrib.middlewares.i18n import I18nMiddleware

from data.config import config
import logging

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.logging.level),
    format=config.logging.format,
    handlers=[
        logging.FileHandler(config.logging.file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class BotLoader:
    """Класс для загрузки и инициализации бота"""
    
    def __init__(self):
        self.bot = None
        self.dp = None
        self.storage = None
        
    def setup_storage(self):
        """Настройка хранилища состояний"""
        if config.redis.use_redis:
            try:
                self.storage = RedisStorage2(
                    host=config.redis.host,
                    port=config.redis.port,
                    db=config.redis.db,
                    password=config.redis.password
                )
                logger.info("Using Redis storage")
            except Exception as e:
                logger.warning(f"Redis not available: {e}")
                self.storage = MemoryStorage()
        else:
            self.storage = MemoryStorage()
            logger.info("Using Memory storage")
    
    def setup_bot(self):
        """Инициализация бота"""
        self.bot = Bot(
            token=config.bot.token,
            parse_mode=types.ParseMode.HTML
        )
        logger.info("Bot initialized")
    
    def setup_dispatcher(self):
        """Инициализация диспетчера"""
        self.dp = Dispatcher(self.bot, storage=self.storage)
        logger.info("Dispatcher initialized")
    
    def setup_middleware(self):
        """Настройка middleware"""
        # Логирование
        self.dp.middleware.setup(LoggingMiddleware())
        
        # Интернационализация (опционально)
        # i18n = I18nMiddleware('bot', 'locales')
        # self.dp.middleware.setup(i18n)
        
        logger.info("Middleware setup completed")
    
    def setup_filters(self):
        """Настройка фильтров"""
        from filters.admin_filter import AdminFilter
        from filters.user_filter import UserFilter
        
        # Регистрация фильтров
        self.dp.filters_factory.bind(AdminFilter)
        self.dp.filters_factory.bind(UserFilter)
        
        logger.info("Filters setup completed")
    
    def load_handlers(self):
        """Загрузка обработчиков"""
        # Импорт всех обработчиков
        import handlers
        
        logger.info("Handlers loaded")
    
    def setup_commands(self):
        """Настройка команд бота"""
        commands = [
            ("start", "🚀 Запустить бота"),
            ("menu", "🏠 Главное меню"),
            ("help", "❓ Помощь"),
            ("about", "ℹ️ О боте"),
            ("profile", "👤 Профиль"),
            ("settings", "⚙️ Настройки"),
            ("commands", "📋 Все команды"),
            ("feedback", "💬 Отзыв"),
            ("support", "🔗 Поддержка"),
            ("version", "📦 Версия"),
            ("status", "📊 Статус"),
            ("ping", "🏓 Проверить соединение"),
            ("uptime", "⏱ Время работы"),
        ]
        
        # Админские команды
        admin_commands = [
            ("ban_user", "🚫 Забанить пользователя"),
            ("unban_user", "✅ Разбанить пользователя"),
            ("stats", "📊 Статистика"),
            ("users", "👥 Пользователи"),
            ("broadcast", "📢 Рассылка"),
            ("settings", "⚙️ Настройки бота"),
            ("backup", "💾 Резервная копия"),
            ("restore", "🔄 Восстановление"),
            ("logs", "📝 Логи"),
            ("restart", "🔄 Перезапуск"),
        ]
        
        return commands, admin_commands
    
    def initialize(self):
        """Полная инициализация бота"""
        logger.info("Starting bot initialization...")
        
        self.setup_storage()
        self.setup_bot()
        self.setup_dispatcher()
        self.setup_middleware()
        self.setup_filters()
        self.load_handlers()
        
        logger.info("Bot initialization completed")
        return self.bot, self.dp


# Создаем экземпляр загрузчика
loader = BotLoader()
bot, dp = loader.initialize()

# Экспорт для использования в других модулях
__all__ = ['bot', 'dp', 'loader', 'config']
