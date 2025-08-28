import logging
import os
from datetime import datetime

from peewee import *
from utils.db_api.sqlite import db

logger = logging.getLogger(__name__)


class Migration(BaseModel):
    """Модель для отслеживания миграций"""

    name = CharField(unique=True, verbose_name='Название миграции')
    applied_at = DateTimeField(default=datetime.now, verbose_name='Дата применения')
    checksum = CharField(verbose_name='Контрольная сумма')

    class Meta:
        table_name = 'migrations'


class MigrationManager:
    """Менеджер миграций"""

    def __init__(self, db_instance, migrations_dir='migrations'):
        self.db = db_instance
        self.migrations_dir = migrations_dir
        self.ensure_migrations_table()

    def ensure_migrations_table(self):
        """Создает таблицу миграций если её нет"""
        if not self.db.table_exists('migrations'):
            self.db.create_tables([Migration])
            logger.info("Created migrations table")

    def get_applied_migrations(self):
        """Получает список примененных миграций"""
        return [m.name for m in Migration.select()]

    def get_pending_migrations(self):
        """Получает список ожидающих миграций"""
        applied = set(self.get_applied_migrations())
        pending = []

        if not os.path.exists(self.migrations_dir):
            return pending

        for filename in sorted(os.listdir(self.migrations_dir)):
            if filename.endswith('.sql'):
                migration_name = filename[:-4]  # Убираем .sql
                if migration_name not in applied:
                    pending.append(migration_name)

        return pending

    def apply_migration(self, migration_name):
        """Применяет миграцию"""
        migration_file = os.path.join(self.migrations_dir, f"{migration_name}.sql")

        if not os.path.exists(migration_file):
            raise FileNotFoundError(f"Migration file not found: {migration_file}")

        try:
            # Читаем SQL файл
            with open(migration_file, 'r', encoding='utf-8') as f:
                sql = f.read()

            # Выполняем миграцию
            self.db.execute_sql(sql)

            # Записываем информацию о миграции
            Migration.create(
                name=migration_name,
                checksum=self._calculate_checksum(sql)
            )

            logger.info(f"Applied migration: {migration_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply migration {migration_name}: {e}")
            raise

    def rollback_migration(self, migration_name):
        """Откатывает миграцию"""
        rollback_file = os.path.join(
            self.migrations_dir, f"{migration_name}_rollback.sql"
        )

        if not os.path.exists(rollback_file):
            raise FileNotFoundError(f"Rollback file not found: {rollback_file}")

        try:
            # Читаем SQL файл отката
            with open(rollback_file, 'r', encoding='utf-8') as f:
                sql = f.read()

            # Выполняем откат
            self.db.execute_sql(sql)

            # Удаляем запись о миграции
            Migration.delete().where(Migration.name == migration_name).execute()

            logger.info(f"Rolled back migration: {migration_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to rollback migration {migration_name}: {e}")
            raise

    def migrate(self):
        """Применяет все ожидающие миграции"""
        pending = self.get_pending_migrations()

        if not pending:
            logger.info("No pending migrations")
            return

        logger.info(f"Found {len(pending)} pending migrations")

        for migration_name in pending:
            self.apply_migration(migration_name)

        logger.info("All migrations applied successfully")

    def create_migration(self, name, description=""):
        """Создает новую миграцию"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        migration_name = f"{timestamp}_{name}"

        # Создаем директорию если её нет
        os.makedirs(self.migrations_dir, exist_ok=True)

        # Создаем файл миграции
        migration_file = os.path.join(self.migrations_dir, f"{migration_name}.sql")
        rollback_file = os.path.join(self.migrations_dir, f"{migration_name}_rollback.sql")

        # Шаблон для миграции
        migration_template = f"""-- Migration: {migration_name}
-- Description: {description}
-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

-- Add your SQL here
-- Example:
-- CREATE TABLE IF NOT EXISTS example_table (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

"""

        # Шаблон для отката
        rollback_template = f"""-- Rollback for: {migration_name}
-- Description: {description}

-- Add your rollback SQL here
-- Example:
-- DROP TABLE IF EXISTS example_table;

"""

        # Записываем файлы
        with open(migration_file, 'w', encoding='utf-8') as f:
            f.write(migration_template)

        with open(rollback_file, 'w', encoding='utf-8') as f:
            f.write(rollback_template)

        logger.info(f"Created migration: {migration_file}")
        logger.info(f"Created rollback: {rollback_file}")

        return migration_name

    def _calculate_checksum(self, content):
        """Вычисляет контрольную сумму содержимого"""
        import hashlib
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def status(self):
        """Показывает статус миграций"""
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()

        print("=== Migration Status ===")
        print(f"Applied: {len(applied)}")
        print(f"Pending: {len(pending)}")

        if applied:
            print("\nApplied migrations:")
            for migration in applied:
                print(f"  ✅ {migration}")

        if pending:
            print("\nPending migrations:")
            for migration in pending:
                print(f"  ⏳ {migration}")

        print("=======================")


# Создаем менеджер миграций
migration_manager = MigrationManager(db)
