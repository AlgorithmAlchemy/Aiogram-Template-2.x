import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    path: str = os.getenv('DB_PATH', 'data/botBD.db')
    type: str = os.getenv('DB_TYPE', 'sqlite')
    host: Optional[str] = os.getenv('DB_HOST')
    port: int = int(os.getenv('DB_PORT', '5432'))
    username: Optional[str] = os.getenv('DB_USERNAME')
    password: Optional[str] = os.getenv('DB_PASSWORD')
    name: Optional[str] = os.getenv('DB_NAME')


@dataclass
class RedisConfig:
    host: str = os.getenv('REDIS_HOST', 'localhost')
    port: int = int(os.getenv('REDIS_PORT', '6379'))
    db: int = int(os.getenv('REDIS_DB', '0'))
    password: Optional[str] = os.getenv('REDIS_PASSWORD')
    use_redis: bool = os.getenv('USE_REDIS', 'false').lower() == 'true'


@dataclass
class LoggingConfig:
    level: str = os.getenv('LOG_LEVEL', 'INFO')
    file: str = os.getenv('LOG_FILE', 'bot.log')
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    max_size: int = int(os.getenv('LOG_MAX_SIZE', '10485760'))  # 10MB
    backup_count: int = int(os.getenv('LOG_BACKUP_COUNT', '5'))


@dataclass
class BotConfig:
    token: str = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    name: str = os.getenv('BOT_NAME', 'Aiogram Template Bot')
    description: str = os.getenv(
        'BOT_DESCRIPTION', 'Powerful Telegram bot template'
    )
    version: str = os.getenv('BOT_VERSION', '1.0.0')
    owner: str = os.getenv('BOT_OWNER', '@your_username')
    support: str = os.getenv('SUPPORT_USERNAME', '@support_username')
    timezone: str = os.getenv('TIMEZONE', 'Europe/Moscow')

    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    timeout: int = int(os.getenv('TIMEOUT', '30'))
    page_size: int = int(os.getenv('PAGE_SIZE', '10'))

    webhook_url: Optional[str] = os.getenv('WEBHOOK_URL')
    webhook_path: str = os.getenv('WEBHOOK_PATH', '/webhook')
    webhook_port: int = int(os.getenv('WEBHOOK_PORT', '8000'))


@dataclass
class AdminConfig:
    owner_ids: List[int] = None

    def __post_init__(self):
        if self.owner_ids is None:
            owner_ids_str = os.getenv(
                'OWNER_IDS', 'YOUR_ADMIN_ID_HERE'
            )
            if owner_ids_str != 'YOUR_ADMIN_ID_HERE':
                self.owner_ids = [int(id.strip()) for id in owner_ids_str.split(',')]
            else:
                self.owner_ids = []


class Config:
    def __init__(self):
        self.bot = BotConfig()
        self.admin = AdminConfig()
        self.database = DatabaseConfig()
        self.redis = RedisConfig()
        self.logging = LoggingConfig()

        self.chat_id = os.getenv('CHAT_ID', 'YOUR_CHAT_ID_HERE')
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'

        self.admin_help_text = """
<b>🔧 Панель администратора</b>

<b>Основные команды:</b>
/ban_user - Забанить пользователя
/unban_user - Разбанить пользователя
/stats - Статистика бота
/users - Список пользователей
/broadcast - Отправить рассылку
/settings - Настройки бота
/backup - Создать резервную копию
/restore - Восстановить из резервной копии
/logs - Показать логи
/restart - Перезапустить бота

<b>Управление пользователями:</b>
/warn_user - Предупредить пользователя
/mute_user - Замутить пользователя
/unmute_user - Размутить пользователя
/delete_user - Удалить пользователя из БД
/user_info - Информация о пользователе
"""

        self.help_text = """
<b>🤖 Помощь по боту</b>

<b>Основные команды:</b>
/start - Запустить бота
/menu - Главное меню
/help - Показать эту справку
/about - Информация о боте
/profile - Ваш профиль
/settings - Настройки
/commands - Все команды

<b>Дополнительные команды:</b>
/feedback - Отправить отзыв
/support - Связаться с поддержкой
/version - Версия бота
/status - Статус бота
/ping - Проверить соединение
/uptime - Время работы бота

<b>Поддержка:</b> {support}
""".format(support=self.bot.support)

config = Config()

API_TOKEN = config.bot.token
OWNER = config.admin.owner_ids
CHAT = config.chat_id
SUPPORT = config.bot.support
admin_help_ru = config.admin_help_text
help_rus = config.help_text
