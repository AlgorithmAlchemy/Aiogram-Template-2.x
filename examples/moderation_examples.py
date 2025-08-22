"""
Примеры использования команд модерации
"""
from models.user import User
from models.sqlite3_creator import connect
import logging

logger = logging.getLogger(__name__)


def example_ban_operations():
    """Примеры операций с банами"""
    
    try:
        # Получаем пользователя
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        print(f"Пользователь: {user}")
        print(f"Статус бана: {user.is_banned}")
        
        # Баним пользователя
        if not user.is_banned:
            user.ban()
            print("Пользователь заблокирован")
        else:
            print("Пользователь уже заблокирован")
        
        # Разбаниваем пользователя
        if user.is_banned:
            user.unban()
            print("Пользователь разблокирован")
        else:
            print("Пользователь не заблокирован")
            
    except Exception as e:
        logger.error(f"Error with ban operations: {e}")


def example_warning_operations():
    """Примеры операций с предупреждениями"""
    
    try:
        # Получаем пользователя
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        print(f"Пользователь: {user}")
        print(f"Предупреждения: {user.warnings}/{user.max_warnings}")
        
        # Добавляем предупреждение
        if user.can_be_warned():
            user.add_warning()
            print(f"Добавлено предупреждение: {user.warnings}/{user.max_warnings}")
        else:
            print("Достигнут максимум предупреждений")
        
        # Убираем предупреждение
        if user.warnings > 0:
            user.remove_warning()
            print(f"Убрано предупреждение: {user.warnings}/{user.max_warnings}")
        else:
            print("Нет предупреждений для удаления")
            
    except Exception as e:
        logger.error(f"Error with warning operations: {e}")


def example_user_status_checks():
    """Примеры проверки статуса пользователя"""
    
    try:
        # Получаем пользователя
        user = User.get_or_none(User.user_id == 123456789)
        if not user:
            print("Пользователь не найден")
            return
        
        print(f"Пользователь: {user}")
        print(f"Активен: {user.is_active()}")
        print(f"Забанен: {user.is_banned}")
        print(f"Замучен: {user.is_muted}")
        print(f"Может быть предупрежден: {user.can_be_warned()}")
        
        # Проверяем различные статусы
        if user.is_banned:
            print("Пользователь заблокирован")
        elif user.is_muted:
            print("Пользователь замучен")
        elif user.warnings >= user.max_warnings:
            print("Пользователь имеет максимальное количество предупреждений")
        else:
            print("Пользователь активен")
            
    except Exception as e:
        logger.error(f"Error with status checks: {e}")


def example_moderation_statistics():
    """Примеры статистики модерации"""
    
    try:
        # Общая статистика
        total_users = User.select().count()
        banned_users = User.select().where(User.is_banned).count()
        muted_users = User.select().where(User.is_muted).count()
        warned_users = User.select().where(User.warnings > 0).count()
        
        print("=== Статистика модерации ===")
        print(f"Всего пользователей: {total_users}")
        print(f"Заблокированных: {banned_users}")
        print(f"Замученных: {muted_users}")
        print(f"С предупреждениями: {warned_users}")
        
        # Пользователи с максимальными предупреждениями
        max_warned = User.select().where(
            User.warnings >= User.max_warnings
        ).count()
        print(f"С максимальными предупреждениями: {max_warned}")
        
        # Активные пользователи
        active_users = User.select().where(
            User.is_banned == False,
            User.is_muted == False
        ).count()
        print(f"Активных пользователей: {active_users}")
        
    except Exception as e:
        logger.error(f"Error with moderation statistics: {e}")


def example_bulk_operations():
    """Примеры массовых операций"""
    
    try:
        # Разбанить всех пользователей
        banned_count = User.select().where(User.is_banned).count()
        if banned_count > 0:
            User.update(is_banned=False).where(User.is_banned).execute()
            print(f"Разблокировано {banned_count} пользователей")
        
        # Сбросить все предупреждения
        warned_count = User.select().where(User.warnings > 0).count()
        if warned_count > 0:
            User.update(warnings=0).where(User.warnings > 0).execute()
            print(f"Сброшены предупреждения у {warned_count} пользователей")
        
        # Размутить всех пользователей
        muted_count = User.select().where(User.is_muted).count()
        if muted_count > 0:
            User.update(is_muted=False).where(User.is_muted).execute()
            print(f"Размучено {muted_count} пользователей")
            
    except Exception as e:
        logger.error(f"Error with bulk operations: {e}")


def main():
    """Основная функция для демонстрации"""
    print("=== Примеры модерации ===")
    
    # Инициализация базы данных
    connect()
    
    # Примеры операций
    example_ban_operations()
    print()
    
    example_warning_operations()
    print()
    
    example_user_status_checks()
    print()
    
    example_moderation_statistics()
    print()
    
    example_bulk_operations()
    print()
    
    print("=== Демонстрация завершена ===")


if __name__ == "__main__":
    main()
