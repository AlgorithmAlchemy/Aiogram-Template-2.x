import datetime
import os
from dotenv import load_dotenv

from aiogram.utils.markdown import text, link

# Загружаем переменные окружения из .env файла
load_dotenv()

# ===== ОСНОВНЫЕ НАСТРОЙКИ БОТА =====
# Получаем конфиденциальные данные из переменных окружения
API_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Получаем ID администраторов из переменной окружения
owner_ids_str = os.getenv('OWNER_IDS', 'YOUR_ADMIN_ID_HERE')
if owner_ids_str != 'YOUR_ADMIN_ID_HERE':
    OWNER = [int(id.strip()) for id in owner_ids_str.split(',')]
else:
    OWNER = ['YOUR_ADMIN_ID_HERE']

# Получаем ID чата из переменной окружения
CHAT = os.getenv('CHAT_ID', 'YOUR_CHAT_ID_HERE')

# Получаем username поддержки из переменной окружения
support_username = os.getenv('SUPPORT_USERNAME', 'YOUR_SUPPORT_USERNAME')
if support_username != 'YOUR_SUPPORT_USERNAME':
    SUPPORT = f'@{support_username}'
else:
    SUPPORT = '@YOUR_SUPPORT_USERNAME'

# ===== НАСТРОЙКИ БОТА =====
# Название бота
BOT_NAME = os.getenv('BOT_NAME', 'My Aiogram Bot')

# Описание бота
BOT_DESCRIPTION = os.getenv('BOT_DESCRIPTION',
                            'A powerful Telegram bot built with aiogram 2.x')

# Версия бота
BOT_VERSION = os.getenv('BOT_VERSION', '1.0.0')

# Владелец бота
BOT_OWNER = os.getenv('BOT_OWNER', '@your_username')

# ===== НАСТРОЙКИ БАЗЫ ДАННЫХ =====
DB_PATH = os.getenv('DB_PATH', 'data/botBD.db')

# ===== НАСТРОЙКИ ЛОГИРОВАНИЯ =====
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# ===== НАСТРОЙКИ ВРЕМЕННОЙ ЗОНЫ =====
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Moscow')

# ===== ТЕКСТЫ СПРАВОК =====
admin_help_ru = """
<b>Панель администратора</b>

Доступные команды:
/ban_user - Забанить пользователя
/help - Показать эту справку
/stats - Статистика бота
/users - Список пользователей
"""

help_rus = """
<b>Справка по боту</b>

Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/profile - Ваш профиль
/settings - Настройки

<b>Поддержка:</b> {support}
""".format(support=SUPPORT)

# ===== ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ =====
# Максимальное количество попыток для некоторых операций
MAX_RETRIES = 3

# Таймаут для операций (в секундах)
TIMEOUT = 30

# Размер страницы для пагинации
PAGE_SIZE = 10
