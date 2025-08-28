import logging
import os

from peewee import SqliteDatabase

logger = logging.getLogger(__name__)


def create_database_connection() -> SqliteDatabase:
    """Создает подключение к базе данных SQLite"""
    # Создаем директорию для базы данных, если её нет
    data_dir: str = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created data directory: {data_dir}")

    # Путь к файлу базы данных
    path_to_db: str = os.path.join(data_dir, "botBD.db")
    logger.info(f"Database path: {path_to_db}")

    # Создаем подключение к базе данных
    db: SqliteDatabase = SqliteDatabase(
        path_to_db,
        pragmas={
            # Write-Ahead Logging для лучшей производительности
            'journal_mode': 'wal',
            'cache_size': -64 * 1000,  # 64MB cache
            'foreign_keys': 1,  # Включаем проверку внешних ключей
            'ignore_check_constraints': 0,  # Проверяем ограничения
            # Отключаем синхронизацию для лучшей производительности
            'synchronous': 0,
            'temp_store': 2,  # Используем память для временных таблиц
        }
    )

    logger.info("Database connection created successfully")
    return db


# Создаем глобальный экземпляр базы данных
db: SqliteDatabase = create_database_connection()
