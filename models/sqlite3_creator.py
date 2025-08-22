"""
Создание таблиц базы данных с использованием Peewee ORM
"""
from peewee import *
from utils.db_api.sqlite import db
from models.user import User, UserSettings, UserStats
import logging

logger = logging.getLogger(__name__)


def connect():
    """Подключение к базе данных и создание таблиц"""
    try:
        # Подключаемся к базе данных
        db.connect()
        
        # Создаем таблицы
        db.create_tables([
            User,
            UserSettings, 
            UserStats
        ], safe=True)
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    finally:
        # Закрываем соединение
        if not db.is_closed():
            db.close()


def create_backup():
    """Создание резервной копии базы данных"""
    try:
        import shutil
        import os
        from datetime import datetime
        
        # Путь к основной базе данных
        db_path = "data/botBD.db"
        
        # Путь для резервной копии
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{backup_dir}/botBD_backup_{timestamp}.db"
        
        # Копируем файл базы данных
        shutil.copy2(db_path, backup_path)
        
        logger.info(f"Database backup created: {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.error(f"Error creating database backup: {e}")
        return None


if __name__ == "__main__":
    # Создаем таблицы при запуске скрипта
    connect()
    print("Database setup completed!")
