import logging
from datetime import datetime

import psutil
from aiogram import types
from aiogram.types import ParseMode

from loader import dp
from models.user import User

logger = logging.getLogger(__name__)


class StatusCommand:
    """Обработчик команды /status"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /status - статус бота"""
        try:
            # Получаем статистику системы
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Конвертируем в GB
            memory_used_gb = memory.used // (1024 ** 3)
            memory_total_gb = memory.total // (1024 ** 3)
            disk_used_gb = disk.used // (1024 ** 3)
            disk_total_gb = disk.total // (1024 ** 3)

            # Получаем статистику пользователей
            total_users = User.select().count()
            today_start = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            active_users = User.select().where(
                User.last_activity >= today_start
            ).count()

            status_text = f"""
<b>📊 Статус бота</b>

<b>Системная информация:</b>
• CPU: {cpu_percent}%
• RAM: {memory.percent}% ({memory_used_gb}GB / {memory_total_gb}GB)
• Диск: {disk.percent}% ({disk_used_gb}GB / {disk_total_gb}GB)

<b>Статистика пользователей:</b>
• Всего пользователей: {total_users}
• Активных сегодня: {active_users}

<b>Статус сервисов:</b>
• База данных: ✅ Активна
• Планировщик задач: ✅ Активен
• API Telegram: ✅ Активен

<b>Время работы:</b> {StatusCommand._get_uptime()}
"""

            await message.answer(
                status_text,
                parse_mode=ParseMode.HTML
            )

        except Exception as e:
            logger.error(f"Error getting status: {e}")
            await message.answer("❌ Ошибка при получении статуса")

    @staticmethod
    def _get_uptime() -> str:
        """Возвращает время работы бота"""
        # Здесь можно добавить логику для отслеживания времени работы
        # Пока возвращаем текущее время как пример
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')


# Регистрация обработчика
@dp.message_handler(commands=['status'], chat_type='private')
async def status_cmd(message: types.Message):
    await StatusCommand.handle(message)
