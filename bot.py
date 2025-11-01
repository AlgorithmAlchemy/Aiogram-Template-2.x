import logging
from datetime import datetime
from typing import List, Optional

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from data.config import config
from loader import bot, dp
from models.migrations import MigrationManager
from models.sqlite3_creator import DatabaseManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format=config.logging.format,
        handlers=[
            logging.FileHandler(config.logging.file),
            logging.StreamHandler()
        ]
    )

class BotManager:
    def __init__(self, bot: Bot, dp: Dispatcher) -> None:
        self.bot: Bot = bot
        self.dp: Dispatcher = dp
        self.start_time: Optional[datetime] = None

    async def on_startup(self, dp: Dispatcher) -> None:
        self.start_time = datetime.now()
        logger.info("Bot starting up...")

        try:
            await self.register_handlers()
            logger.info("Handlers registered successfully")

            await self.setup_middleware()
            logger.info("Middleware setup completed")

            await self.setup_filters()
            logger.info("Filters setup completed")

            await self.setup_error_handlers()
            logger.info("Error handlers setup completed")

            logger.info(f"Bot started successfully at {self.start_time}")

        except Exception as e:
            logger.error(f"Error during startup: {e}")
            raise

    async def on_shutdown(self, dp: Dispatcher) -> None:
        logger.info("Bot shutting down...")

        try:
            # Closing Connections
            await self.bot.session.close()
            logger.info("Bot session closed")

            # Additional cleaning if needed
            if self.start_time:
                uptime = datetime.now() - self.start_time
                logger.info(f"Bot stopped. Uptime: {uptime}")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

    async def register_handlers(self) -> None:
        try:
            from handlers.users.message.commands.start import StartCommandHandler
            from handlers.users.message.commands.profile import ProfileCommandHandler
            from handlers.users.message.commands.ban_user import BanUserCommandHandler
            from handlers.users.message.commands.unban_user import UnbanUserCommandHandler
            from handlers.users.message.commands.warn_user import WarnUserCommandHandler
            from handlers.users.message.commands.weather import WeatherCommandHandler
            from handlers.users.message.echo import EchoMessageHandler

            # Creating handler instances for automatic registration
            handlers: List[object] = [
                StartCommandHandler(self.dp),
                ProfileCommandHandler(self.dp),
                BanUserCommandHandler(self.dp),
                UnbanUserCommandHandler(self.dp),
                WarnUserCommandHandler(self.dp),
                WeatherCommandHandler(self.dp),
                EchoMessageHandler(self.dp),
            ]

            logger.info(f"Registered {len(handlers)} handlers")

        except Exception as e:
            logger.error(f"Error registering handlers: {e}")
            raise

    async def setup_middleware(self) -> None:
        try:
            from middleware.logging import LoggingMiddleware
            from middleware.throttling import ThrottlingMiddleware
            from middleware.admin import AdminMiddleware
            from middleware.database import DatabaseMiddleware

            self.dp.middleware.setup(LoggingMiddleware())
            self.dp.middleware.setup(ThrottlingMiddleware(rate_limit=0.5))
            self.dp.middleware.setup(AdminMiddleware())
            self.dp.middleware.setup(DatabaseMiddleware())

            logger.info("Custom middleware registered successfully")
        except Exception as e:
            logger.error(f"Error setting up middleware: {e}")
            raise

    async def setup_filters(self) -> None:
        try:
            logger.info("Filters setup completed")
        except Exception as e:
            logger.error(f"Error setting up filters: {e}")
            raise

    async def setup_error_handlers(self) -> None:
        try:
            @self.dp.errors_handler()
            async def errors_handler(
                    update: types.Update,
                    exception: Exception
            ) -> bool:
                logger.error(f"Update: {update}")
                logger.error(f"Exception: {exception}")
                return True

            logger.info("Error handlers setup completed")
        except Exception as e:
            logger.error(f"Error setting up error handlers: {e}")
            raise


bot_manager = BotManager(bot, dp)

setup_logging()

if __name__ == '__main__':
    logger.info("Starting bot...")

    # Configuring allowed_updates for aiogram 2.x
    allowed_updates = [
        'message',
        'edited_message',
        'channel_post',
        'edited_channel_post',
        'inline_query',
        'chosen_inline_result',
        'callback_query',
        'shipping_query',
        'pre_checkout_query',
        'poll',
        'poll_answer',
        'my_chat_member',
        'chat_member',
        'chat_join_request'
    ]

    executor.start_polling(
        dispatcher=dp,
        on_startup=bot_manager.on_startup,
        on_shutdown=bot_manager.on_shutdown,
        allowed_updates=allowed_updates,
        skip_updates=True
    )
