from aiogram import executor
from aiogram.types import AllowedUpdates
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

from models.sqlite3_creator import db, connect
from loader import dp, bot
import filters, handlers, models, states

# Настройка логирования
logger = logging.getLogger(__name__)

# Инициализация планировщика задач
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

def setup_scheduler():
    """Настройка планировщика задач"""
    # Пример добавления задачи
    # scheduler.add_job(your_function, trigger='interval', hours=1)
    scheduler.start()
    logger.info("Scheduler started")

async def on_startup(dp):
    """Действия при запуске бота"""
    logger.info("Bot starting up...")
    
    # Подключение к базе данных
    try:
        connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    
    # Запуск планировщика
    setup_scheduler()
    
    # Установка команд бота
    await bot.set_my_commands([
        ("start", "Запустить бота"),
        ("help", "Показать справку"),
        ("profile", "Ваш профиль"),
        ("settings", "Настройки")
    ])
    
    logger.info("Bot started successfully!")

async def on_shutdown(dp):
    """Действия при остановке бота"""
    logger.info("Bot shutting down...")
    
    # Остановка планировщика
    scheduler.shutdown()
    
    # Закрытие соединений
    await bot.session.close()
    
    logger.info("Bot stopped successfully!")

if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(
        dp,
        skip_updates=True,
        allowed_updates=AllowedUpdates.all(),
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
