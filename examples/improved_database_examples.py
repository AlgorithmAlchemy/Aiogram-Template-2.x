"""
Примеры использования улучшенной архитектуры базы данных
"""
from datetime import datetime, timedelta
from models.user import (
    User, UserSettings, UserStats, UserWarning, 
    UserBan, UserUnban, UserMute, UserUnmute
)
from models.sqlite3_creator import db_manager
import logging

logger = logging.getLogger(__name__)


def example_user_operations():
    """Примеры операций с пользователями"""
    
    try:
        # Создание нового пользователя
        user = User.create(
            user_id=123456789,
            username="test_user",
            first_name="Тест",
            last_name="Пользователь",
            language_code="ru",
            is_premium=True
        )
        print(f"Создан пользователь: {user}")
        
        # Получение пользователя
        user = User.get_or_none(User.user_id == 123456789)
        if user:
            print(f"Найден пользователь: {user}")
            
            # Обновление пользователя
            user.first_name = "Обновленное имя"
            user.save()
            print(f"Пользователь обновлен: {user}")
            
            # Создание настроек и статистики
            settings = user.get_settings()
            stats = user.get_stats()
            print(f"Настройки: {settings}")
            print(f"Статистика: {stats}")
        
    except Exception as e:
        logger.error(f"Error with user operations: {e}")


def example_moderation_operations():
    """Примеры операций модерации"""
    
    try:
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        print(f"Пользователь: {user}")
        print(f"Статус: {'Активен' if user.is_active_user() else 'Неактивен'}")
        
        # Предупреждения
        if user.can_be_warned():
            user.add_warning("Нарушение правил")
            print(f"Добавлено предупреждение: {user.warnings}/{user.max_warnings}")
        
        # Бан
        if not user.is_banned:
            user.ban("Серьезное нарушение")
            print("Пользователь заблокирован")
        
        # Разбан
        if user.is_banned:
            user.unban()
            print("Пользователь разблокирован")
        
        # Мут
        if not user.is_muted:
            user.mute(duration_minutes=60, reason="Спам")
            print("Пользователь замучен на 60 минут")
        
        # Размут
        if user.is_muted:
            user.unmute()
            print("Пользователь размучен")
        
        # История модерации
        warnings = user.get_warnings_history()
        bans = user.get_ban_history()
        
        print(f"История предупреждений: {len(warnings)} записей")
        print(f"История банов: {len(bans)} записей")
        
    except Exception as e:
        logger.error(f"Error with moderation operations: {e}")


def example_statistics_operations():
    """Примеры операций со статистикой"""
    
    try:
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        stats = user.get_stats()
        
        # Обновление статистики
        user.update_activity()
        stats.increment_messages(len("Тестовое сообщение"))
        stats.increment_commands()
        stats.increment_files('photo')
        stats.increment_files('document')
        
        print(f"Статистика обновлена:")
        print(f"  Сообщений: {stats.messages_sent}")
        print(f"  Команд: {stats.commands_used}")
        print(f"  Файлов: {stats.files_sent}")
        print(f"  Фото: {stats.photos_sent}")
        print(f"  Документов: {stats.documents_sent}")
        print(f"  Средняя длина сообщения: {stats.average_message_length}")
        
    except Exception as e:
        logger.error(f"Error with statistics operations: {e}")


def example_advanced_queries():
    """Примеры сложных запросов"""
    
    try:
        # Активные пользователи
        active_users = User.select().where(
            User.is_active == True,
            User.is_banned == False,
            User.is_muted == False
        )
        print(f"Активных пользователей: {active_users.count()}")
        
        # Пользователи с предупреждениями
        warned_users = User.select().where(User.warnings > 0)
        print(f"Пользователей с предупреждениями: {warned_users.count()}")
        
        # Забаненные пользователи
        banned_users = User.select().where(User.is_banned == True)
        print(f"Забаненных пользователей: {banned_users.count()}")
        
        # Пользователи за последние 7 дней
        week_ago = datetime.now() - timedelta(days=7)
        recent_users = User.select().where(User.created_at >= week_ago)
        print(f"Новых пользователей за неделю: {recent_users.count()}")
        
        # Самые активные пользователи
        active_users = User.select().order_by(User.messages_count.desc()).limit(5)
        print("Топ-5 активных пользователей:")
        for user in active_users:
            print(f"  {user.first_name}: {user.messages_count} сообщений")
        
        # Пользователи с максимальными предупреждениями
        max_warned = User.select().where(
            User.warnings >= User.max_warnings
        )
        print(f"Пользователей с макс. предупреждениями: {max_warned.count()}")
        
    except Exception as e:
        logger.error(f"Error with advanced queries: {e}")


def example_database_management():
    """Примеры управления базой данных"""
    
    try:
        # Информация о базе данных
        info = db_manager.get_database_info()
        if info:
            print("=== Информация о базе данных ===")
            print(f"Путь: {info['database_path']}")
            print(f"Всего записей: {info['total_records']}")
            print("Таблицы:")
            for table in info['tables']:
                print(f"  {table['name']}: {table['records']} записей")
        
        # Проверка целостности
        if db_manager.check_integrity():
            print("✅ Целостность базы данных в порядке")
        else:
            print("❌ Проблемы с целостностью базы данных")
        
        # Создание резервной копии
        backup_path = db_manager.create_backup()
        if backup_path:
            print(f"✅ Резервная копия создана: {backup_path}")
        
        # Оптимизация базы данных
        db_manager.optimize_database()
        print("✅ База данных оптимизирована")
        
    except Exception as e:
        logger.error(f"Error with database management: {e}")


def example_bulk_operations():
    """Примеры массовых операций"""
    
    try:
        # Создание тестовых пользователей
        test_users = []
        for i in range(1, 6):
            user = User.create(
                user_id=100000000 + i,
                username=f"test_user_{i}",
                first_name=f"Тест{i}",
                last_name="Пользователь",
                language_code="ru"
            )
            test_users.append(user)
        
        print(f"Создано {len(test_users)} тестовых пользователей")
        
        # Массовое обновление
        User.update(
            language_code="en"
        ).where(
            User.username.contains("test_user")
        ).execute()
        
        print("Язык обновлен для тестовых пользователей")
        
        # Массовое удаление (мягкое)
        for user in test_users:
            user.soft_delete()
        
        print("Тестовые пользователи мягко удалены")
        
        # Восстановление
        for user in test_users:
            user.restore()
        
        print("Тестовые пользователи восстановлены")
        
        # Очистка
        for user in test_users:
            user.delete_instance()
        
        print("Тестовые пользователи полностью удалены")
        
    except Exception as e:
        logger.error(f"Error with bulk operations: {e}")


def main():
    """Основная функция для демонстрации"""
    print("=== Демонстрация улучшенной архитектуры БД ===")
    
    # Подключаемся к базе данных
    db_manager.connect()
    
    try:
        # Примеры операций
        example_user_operations()
        print()
        
        example_moderation_operations()
        print()
        
        example_statistics_operations()
        print()
        
        example_advanced_queries()
        print()
        
        example_database_management()
        print()
        
        example_bulk_operations()
        print()
        
    finally:
        # Отключаемся от базы данных
        db_manager.disconnect()
    
    print("=== Демонстрация завершена ===")


if __name__ == "__main__":
    main()
