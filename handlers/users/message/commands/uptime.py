import logging
from datetime import datetime

from aiogram import types
from aiogram.types import ParseMode

from loader import dp

logger = logging.getLogger(__name__)


class UptimeCommand:
    """Обработчик команды /uptime"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /uptime - время работы бота"""
        uptime_text = f"""
<b>⏱️ Время работы бота</b>

<b>Запущен:</b> {UptimeCommand._get_uptime()}

<b>Статус:</b> ✅ Активен
<b>Режим:</b> Polling
<b>Версия:</b> 2.25.2

<i>Бот работает стабильно и готов к работе!</i>
"""

        await message.answer(
            uptime_text,
            parse_mode=ParseMode.HTML
        )

    @staticmethod
    def _get_uptime() -> str:
        """Возвращает время работы бота"""
        # Здесь можно добавить логику для отслеживания времени работы
        # Пока возвращаем текущее время как пример
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')


# Регистрация обработчика
@dp.message_handler(commands=['uptime'], chat_type='private')
async def uptime_cmd(message: types.Message):
    await UptimeCommand.handle(message)
