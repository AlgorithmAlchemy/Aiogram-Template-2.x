from aiogram import executor
from aiogram.types import AllowedUpdates
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import signal
import sys
from datetime import datetime

from data.config import config
from loader import bot, dp, loader
from models.sqlite3_creator import connect
from utils.integration import create_integration
# Импорты для регистрации обработчиков
import filters
import handlers
import models
import states

logger = logging.getLogger(__name__)


class BotManager:
    """Класс для управления ботом"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=config.bot.timezone)
        self.start_time = datetime.now()
        
    async def setup_database(self):
        """Настройка базы данных"""
        try:
            connect()
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def setup_scheduler(self):
        """Настройка планировщика задач"""
        # Пример добавления задач
        # self.scheduler.add_job(
        #     self.daily_stats, trigger='cron', hour=9, minute=0
        # )
        # self.scheduler.add_job(
        #     self.cleanup_old_data, trigger='cron', hour=2, minute=0
        # )
        
        self.scheduler.start()
        logger.info("Scheduler started")
    
    async def setup_commands(self):
        """Настройка команд бота"""
        commands, admin_commands = loader.setup_commands()
        
        try:
            await bot.set_my_commands(commands)
            logger.info("Bot commands set successfully")
        except Exception as e:
            logger.error(f"Failed to set bot commands: {e}")
    
    async def daily_stats(self):
        """Ежедневная статистика"""
        try:
            from models.user import User
            
            total_users = User.select().count()
            active_users = User.select().where(
                User.is_banned == False
            ).count()
            
            stats_text = f"""
<b>📊 Ежедневная статистика</b>

<b>Пользователи:</b>
• Всего: {total_users}
• Активных: {active_users}

<b>Дата:</b> {datetime.now().strftime('%d.%m.%Y')}
"""
            
            # Отправляем статистику администраторам
            for admin_id in config.admin.owner_ids:
                try:
                    await bot.send_message(
                        admin_id, stats_text, parse_mode='HTML'
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to send stats to admin {admin_id}: {e}"
                    )
                    
        except Exception as e:
            logger.error(f"Error in daily stats: {e}")
    
    async def cleanup_old_data(self):
        """Очистка старых данных"""
        try:
            # Здесь можно добавить очистку старых логов,
            # временных файлов и т.д.
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
    
    def get_uptime(self):
        """Получение времени работы бота"""
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}д {hours}ч {minutes}м"
        elif hours > 0:
            return f"{hours}ч {minutes}м"
        else:
            return f"{minutes}м {seconds}с"
    
    async def on_startup(self, dp):
        """Действия при запуске бота"""
        logger.info("Bot starting up...")
        
        # Настройка базы данных
        await self.setup_database()
        
        # Настройка планировщика
        self.setup_scheduler()
        
        # Настройка команд
        await self.setup_commands()
        
        # Интеграция всех компонентов шаблона
        self.integration = create_integration(dp)
        self.integration.setup_all()
        self.integration.execute_startup_hooks()
        
        # Установка обработчиков сигналов
        self.setup_signal_handlers()
        
        logger.info("Bot started successfully!")
    
    async def on_shutdown(self, dp):
        """Действия при остановке бота"""
        logger.info("Bot shutting down...")
        
        # Выполнение shutdown hooks
        if hasattr(self, 'integration'):
            self.integration.execute_shutdown_hooks()
        
        # Остановка планировщика
        self.scheduler.shutdown()
        
        # Закрытие соединений
        await bot.session.close()
        
        logger.info("Bot stopped successfully!")
    
    def setup_signal_handlers(self):
        """Настройка обработчиков сигналов"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


class MiddlewareManager:
    """Класс для управления middleware"""
    
    @staticmethod
    def setup_middleware(dp):
        """Настройка middleware"""
        # Здесь можно добавить дополнительные middleware
        # dp.middleware.setup(CustomMiddleware())
        pass


class ErrorHandler:
    """Класс для обработки ошибок"""
    
    @staticmethod
    async def handle_errors(update, exception):
        """Глобальный обработчик ошибок"""
        logger.error(f"Update {update} caused error {exception}")
        
        # Здесь можно добавить отправку уведомлений администраторам
        # или сохранение ошибок в базу данных
        
        return True


def main():
    """Основная функция запуска бота"""
    # Создаем менеджер бота
    bot_manager = BotManager()
    
    # Настройка middleware
    MiddlewareManager.setup_middleware(dp)
    
    # Настройка обработчика ошибок
    dp.errors_handler()(ErrorHandler.handle_errors)
    
    # Запуск бота
    executor.start_polling(
        dp,
        skip_updates=True,
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
        # ============================================
        on_startup=bot_manager.on_startup,
        on_shutdown=bot_manager.on_shutdown
    )


if __name__ == '__main__':
    main()
