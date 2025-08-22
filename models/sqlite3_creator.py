"""
Создание таблиц базы данных с использованием Peewee ORM
"""
from peewee import *
from database.connection import db
from models.base import BaseModel
from models.user import (
    User, UserSettings, UserStats, UserWarning, 
    UserBan, UserUnban, UserMute, UserUnmute
)
from models.migrations import Migration, migration_manager
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Менеджер базы данных"""
    
    def __init__(self):
        self.db = db
        self.models = [
            # Основные модели
            User,
            UserSettings,
            UserStats,
            
            # Модели модерации
            UserWarning,
            UserBan,
            UserUnban,
            UserMute,
            UserUnmute,
            
            # Системные модели
            Migration,
        ]
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.db.connect()
            logger.info("Connected to database")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def disconnect(self):
        """Отключение от базы данных"""
        if not self.db.is_closed():
            self.db.close()
            logger.info("Disconnected from database")
    
    def create_tables(self):
        """Создание всех таблиц"""
        try:
            self.db.create_tables(self.models, safe=True)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def drop_tables(self):
        """Удаление всех таблиц"""
        try:
            self.db.drop_tables(self.models, safe=True)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping database tables: {e}")
            raise
    
    def reset_database(self):
        """Полный сброс базы данных"""
        try:
            self.drop_tables()
            self.create_tables()
            logger.info("Database reset successfully")
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            raise
    
    def run_migrations(self):
        """Запуск миграций"""
        try:
            migration_manager.migrate()
            logger.info("Migrations completed successfully")
        except Exception as e:
            logger.error(f"Error running migrations: {e}")
            raise
    
    def create_backup(self, backup_path=None):
        """Создание резервной копии базы данных"""
        try:
            import shutil
            import os
            from datetime import datetime
            
            # Путь к основной базе данных
            db_path = "data/botBD.db"
            
            if not backup_path:
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
    
    def get_database_info(self):
        """Получение информации о базе данных"""
        try:
            info = {
                'database_path': self.db.database,
                'tables': [],
                'total_records': 0
            }
            
            # Получаем список таблиц
            cursor = self.db.execute_sql("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                # Подсчитываем количество записей в таблице
                cursor = self.db.execute_sql(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                
                info['tables'].append({
                    'name': table,
                    'records': count
                })
                info['total_records'] += count
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return None
    
    def optimize_database(self):
        """Оптимизация базы данных"""
        try:
            # Анализируем базу данных
            self.db.execute_sql("ANALYZE;")
            
            # Перестраиваем индексы
            self.db.execute_sql("REINDEX;")
            
            # Очищаем свободное место
            self.db.execute_sql("VACUUM;")
            
            logger.info("Database optimized successfully")
            
        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
            raise
    
    def check_integrity(self):
        """Проверка целостности базы данных"""
        try:
            cursor = self.db.execute_sql("PRAGMA integrity_check;")
            result = cursor.fetchone()[0]
            
            if result == "ok":
                logger.info("Database integrity check passed")
                return True
            else:
                logger.error(f"Database integrity check failed: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking database integrity: {e}")
            return False


# Создаем глобальный экземпляр менеджера
db_manager = DatabaseManager()


def connect():
    """Подключение к базе данных и создание таблиц"""
    try:
        db_manager.connect()
        db_manager.create_tables()
        db_manager.run_migrations()
        logger.info("Database setup completed successfully")
    except Exception as e:
        logger.error(f"Error in database setup: {e}")
        raise
    finally:
        db_manager.disconnect()


def create_backup():
    """Создание резервной копии базы данных"""
    return db_manager.create_backup()


def get_database_info():
    """Получение информации о базе данных"""
    return db_manager.get_database_info()


def optimize_database():
    """Оптимизация базы данных"""
    try:
        db_manager.connect()
        db_manager.optimize_database()
    finally:
        db_manager.disconnect()


def check_integrity():
    """Проверка целостности базы данных"""
    try:
        db_manager.connect()
        return db_manager.check_integrity()
    finally:
        db_manager.disconnect()


if __name__ == "__main__":
    # Создаем таблицы при запуске скрипта
    connect()
    
    # Показываем информацию о базе данных
    info = get_database_info()
    if info:
        print("=== Database Information ===")
        print(f"Database: {info['database_path']}")
        print(f"Total records: {info['total_records']}")
        print("\nTables:")
        for table in info['tables']:
            print(f"  {table['name']}: {table['records']} records")
        print("============================")
    
    print("Database setup completed!")
