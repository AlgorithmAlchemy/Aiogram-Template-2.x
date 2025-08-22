"""
Настройки подключения к базе данных SQLite
"""
import os
import logging
from peewee import SqliteDatabase

logger = logging.getLogger(__name__)


def create_database_connection() -> SqliteDatabase:
    """Создает подключение к базе данных SQLite"""
    
    # Создаем директорию для базы данных, если её нет
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created data directory: {data_dir}")

    # Путь к файлу базы данных
    path_to_db = os.path.join(data_dir, "botBD.db")
    logger.info(f"Database path: {path_to_db}")

    # Создаем подключение к базе данных
    db = SqliteDatabase(
        path_to_db,
        pragmas={
            'journal_mode': 'wal',  # Write-Ahead Logging для лучшей производительности
            'cache_size': -64 * 1000,  # 64MB cache
            'foreign_keys': 1,  # Включаем проверку внешних ключей
            'ignore_check_constraints': 0,  # Проверяем ограничения
            'synchronous': 0,  # Отключаем синхронизацию для лучшей производительности
            'temp_store': 2,  # Используем память для временных таблиц
        }
    )
    
    logger.info("Database connection created successfully")
    return db


# Создаем глобальный экземпляр базы данных
db = create_database_connection()
