"""
Настройки базы данных SQLite
"""
from peewee import SqliteDatabase
import os

# Создаем директорию для базы данных, если её нет
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Путь к файлу базы данных
path_to_db = os.path.join(data_dir, "botBD.db")

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
