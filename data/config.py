import datetime
import os
from dotenv import load_dotenv

from aiogram.utils.markdown import text, link

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем конфиденциальные данные из переменных окружения
# Если переменные не найдены, используем значения по умолчанию
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

# Добавляем недостающие переменные, которые используются в коде
admin_help_ru = """
<b>Панель администратора</b>

Доступные команды:
/ban_user - Забанить пользователя
/help - Показать эту справку
"""
help_rus = """
<b>Справка по боту</b>

Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку
"""
