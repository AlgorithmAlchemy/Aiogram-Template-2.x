import logging

from aiogram import types
from aiogram.types import ParseMode

from app.data.config import config
from app.loader import dp

logger = logging.getLogger(__name__)


class AboutCommand:
    """Обработчик команды /about"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /about - информация о боте"""
        about_text = AboutCommand._get_about_text()

        await message.answer(
            about_text,
            parse_mode=ParseMode.HTML
        )

    @staticmethod
    def _get_about_text() -> str:
        """Генерирует текст с информацией о боте"""
        return f"""
<b>ℹ️ О боте</b>

<b>Название:</b> {config.bot.name}
<b>Описание:</b> {config.bot.description}
<b>Версия:</b> {config.bot.version}
<b>Владелец:</b> {config.bot.owner}

<b>Возможности:</b>
• Удобный интерфейс
• Быстрые ответы
• Полезные функции
• Поддержка пользователей

<b>Технологии:</b>
• Python 3.8+
• aiogram 2.25.2
• SQLite + Peewee ORM
• APScheduler

<b>Поддержка:</b> {config.bot.support}
<b>Чат:</b> {config.chat_id}

<b>Статус:</b> ✅ Активен
"""


# Регистрация обработчика
@dp.message_handler(commands=['about'], chat_type='private')
async def about_cmd(message: types.Message):
    await AboutCommand.handle(message)
