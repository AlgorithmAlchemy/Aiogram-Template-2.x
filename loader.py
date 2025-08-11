from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
import logging

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

# Инициализация бота
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)

# Используем MemoryStorage для простоты
# Для продакшена рекомендуется использовать Redis
storage = MemoryStorage()

# Инициализация диспетчера
dp = Dispatcher(bot, storage=storage)

# Экспорт для использования в других модулях
__all__ = ['bot', 'dp', 'storage']
