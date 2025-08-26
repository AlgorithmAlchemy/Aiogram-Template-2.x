from datetime import datetime, timedelta
from models.user import User, UserSettings, UserStats
from models.sqlite3_creator import connect
import logging

logger = logging.getLogger(__name__)


def example_user_operations():
    """Примеры операций с пользователями"""
    
    # 1. Создание нового пользователя
    try:
        user, created = User.get_or_create(
            user_id=123456789,
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johndoe',
                'language_code': 'en',
                'is_bot': False
            }
        )
        
        if created:
            print(f"Создан новый пользователь: {user}")
        else:
            print(f"Пользователь уже существует: {user}")
            
    except Exception as e:
        logger.error(f"Error creating user: {e}")
    
    # 2. Получение пользователя по ID
    try:
        user = User.get_or_none(User.user_id == 123456789)
        if user:
            print(f"Найден пользователь: {user}")
        else:
            print("Пользователь не найден")
    except Exception as e:
        logger.error(f"Error getting user: {e}")
    
    # 3. Обновление пользователя
    try:
        user = User.get(User.user_id == 123456789)
        user.last_activity = datetime.now()
        user.save()
        print("Пользователь обновлен")
    except User.DoesNotExist:
        print("Пользователь не найден")
    except Exception as e:
        logger.error(f"Error updating user: {e}")
    
    # 4. Получение всех пользователей
    try:
        all_users = User.select()
        print(f"Всего пользователей: {all_users.count()}")
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
    
    # 5. Фильтрация пользователей
    try:
        # Активные пользователи (не забаненные)
        active_users = User.select().where(User.is_banned == False)
        print(f"Активных пользователей: {active_users.count()}")
        
        # Пользователи, активные сегодня
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        today_active = User.select().where(
            User.last_activity >= today_start
        )
        print(f"Активных сегодня: {today_active.count()}")
        
        # Пользователи с предупреждениями
        warned_users = User.select().where(User.warnings > 0)
        print(f"Пользователей с предупреждениями: {warned_users.count()}")
        
    except Exception as e:
        logger.error(f"Error filtering users: {e}")


def example_stats_operations():
    """Примеры операций со статистикой"""
    
    try:
        # Получение пользователя
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        # Создание или получение статистики
        stats, created = UserStats.get_or_create(user=user)
        
        if created:
            print("Создана новая статистика")
        else:
            print("Статистика уже существует")
        
        # Обновление статистики
        stats.increment_messages()
        stats.increment_commands()
        stats.increment_photos()
        
        print(f"Статистика обновлена: {stats}")
        
        # Получение общей статистики
        total_messages = sum(
            s.messages_sent for s in UserStats.select()
        )
        total_commands = sum(
            s.commands_used for s in UserStats.select()
        )
        
        print(f"Всего сообщений: {total_messages}")
        print(f"Всего команд: {total_commands}")
        
    except Exception as e:
        logger.error(f"Error with stats operations: {e}")


def example_settings_operations():
    """Примеры операций с настройками"""
    
    try:
        # Получение пользователя
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        # Создание или получение настроек
        settings, created = UserSettings.get_or_create(user=user)
        
        if created:
            print("Созданы новые настройки")
        else:
            print("Настройки уже существуют")
        
        # Обновление настроек
        settings.language = 'en'
        settings.notifications = False
        settings.theme = 'dark'
        settings.save()
        
        print(f"Настройки обновлены: {settings}")
        
    except Exception as e:
        logger.error(f"Error with settings operations: {e}")


def example_complex_queries():
    """Примеры сложных запросов"""
    
    try:
        # Пользователи с наибольшим количеством сообщений
        top_users = (
            User.select(User, UserStats.messages_sent)
            .join(UserStats)
            .order_by(UserStats.messages_sent.desc())
            .limit(5)
        )
        
        print("Топ-5 пользователей по сообщениям:")
        for user in top_users:
            print(f"{user.first_name}: {user.stats.messages_sent} сообщений")
        
        # Статистика по дням
        week_ago = datetime.now() - timedelta(days=7)
        recent_users = User.select().where(
            User.created_at >= week_ago
        ).count()
        
        print(f"Новых пользователей за неделю: {recent_users}")
        
        # Пользователи с настройками
        users_with_settings = (
            User.select()
            .join(UserSettings)
            .where(UserSettings.language == 'en')
        ).count()
        
        print(f"Пользователей с английским языком: {users_with_settings}")
        
    except Exception as e:
        logger.error(f"Error with complex queries: {e}")


def main():
    """Основная функция для демонстрации"""
    print("=== Примеры работы с базой данных ===")
    
    # Инициализация базы данных
    connect()
    
    # Примеры операций
    example_user_operations()
    print()
    
    example_stats_operations()
    print()
    
    example_settings_operations()
    print()
    
    example_complex_queries()
    print()
    
    print("=== Демонстрация завершена ===")


if __name__ == "__main__":
    main()
