import logging

from loader import bot, dp, config

logger = logging.getLogger(__name__)


def basic_usage_example():
    """Пример базового использования loader"""
    print("=== Basic Loader Usage ===")

    # Получаем экземпляры бота и диспетчера
    bot_instance = bot
    dp_instance = dp

    print(f"Bot token: {config.bot.token[:10]}...")
    print(f"Bot username: {bot_instance.username}")
    print(f"Dispatcher: {dp_instance}")
    print(f"Storage: {dp_instance.storage}")

    print("=== Basic Loader Usage Completed ===")


def custom_loader_example():
    """Пример создания кастомного loader"""
    print("=== Custom Loader Example ===")

    from loader import BotLoader

    # Создаем новый экземпляр loader
    custom_loader = BotLoader()

    # Инициализируем с кастомными настройками
    custom_bot, custom_dp = custom_loader.initialize()

    print(f"Custom bot: {custom_bot}")
    print(f"Custom dispatcher: {custom_dp}")

    print("=== Custom Loader Example Completed ===")


def storage_examples():
    """Примеры различных типов хранилищ"""
    print("=== Storage Examples ===")

    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    from aiogram.contrib.fsm_storage.redis import RedisStorage2

    # Memory storage
    memory_storage = MemoryStorage()
    print(f"Memory storage: {memory_storage}")

    # Redis storage (если доступен)
    try:
        redis_storage = RedisStorage2(
            host='localhost',
            port=6379,
            db=0
        )
        print(f"Redis storage: {redis_storage}")
    except Exception as e:
        print(f"Redis not available: {e}")

    print("=== Storage Examples Completed ===")


def config_integration_example():
    """Пример интеграции с конфигурацией"""
    print("=== Config Integration Example ===")

    # Использование конфигурации
    print(f"Bot token: {config.bot.token[:10]}...")
    print(f"Debug mode: {config.debug}")
    print(f"Logging level: {config.logging.level}")

    # Redis настройки
    if config.redis.use_redis:
        print(f"Redis host: {config.redis.host}")
        print(f"Redis port: {config.redis.port}")
    else:
        print("Using memory storage")

    print("=== Config Integration Example Completed ===")


def main():
    """Главная функция для демонстрации"""
    print("=== Loader Examples ===")

    # Примеры использования
    basic_usage_example()
    custom_loader_example()
    storage_examples()
    config_integration_example()

    print("\n=== All Loader Examples Completed ===")


if __name__ == "__main__":
    main()
