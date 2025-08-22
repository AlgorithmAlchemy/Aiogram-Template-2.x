"""
Загрузчик бота - базовая инициализация
"""
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data.config import config
import logging

logger = logging.getLogger(__name__)


class BotLoader:
    """Класс для базовой инициализации бота"""
    
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
    
    def initialize(self):
        """Базовая инициализация бота"""
        logger.info("Starting basic bot initialization...")
        
        self.setup_storage()
        self.setup_bot()
        self.setup_dispatcher()
        
        logger.info("Basic bot initialization completed")
        return self.bot, self.dp


# Создаем экземпляр загрузчика
loader = BotLoader()
bot, dp = loader.initialize()

# Экспорт для использования в других модулях
__all__ = ['bot', 'dp', 'loader', 'config']
