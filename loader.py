import logging
from typing import Tuple, Optional

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data.config import config

logger = logging.getLogger(__name__)


class BotLoader:
    def __init__(self) -> None:
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.storage: Optional[MemoryStorage | RedisStorage2] = None

    def setup_storage(self) -> None:
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

    def setup_bot(self) -> None:
        self.bot = Bot(
            token=config.bot.token,
            parse_mode=types.ParseMode.HTML
        )
        logger.info("Bot initialized")

    def setup_dispatcher(self) -> None:
        if self.bot is None or self.storage is None:
            raise RuntimeError("Bot and storage must be initialized first")

        self.dp = Dispatcher(self.bot, storage=self.storage)
        logger.info("Dispatcher initialized")

    def initialize(self) -> Tuple[Bot, Dispatcher]:
        logger.info("Starting basic bot initialization...")

        self.setup_storage()
        self.setup_bot()
        self.setup_dispatcher()

        if self.bot is None or self.dp is None:
            raise RuntimeError("Failed to initialize bot or dispatcher")

        logger.info("Basic bot initialization completed")
        return self.bot, self.dp

loader = BotLoader()
bot, dp = loader.initialize()

__all__ = ['bot', 'dp', 'loader', 'config']
