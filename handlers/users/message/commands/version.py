from aiogram import types
from aiogram.types import ParseMode
import logging
from datetime import datetime

from data.config import config
from loader import dp

logger = logging.getLogger(__name__)


class VersionCommand:
    """Обработчик команды /version"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /version - версия бота"""
        version_text = f"""
<b>📦 Информация о версии</b>

<b>Версия бота:</b> {config.bot.version}
<b>Название:</b> {config.bot.name}
<b>Описание:</b> {config.bot.description}
<b>Владелец:</b> {config.bot.owner}
<b>Время запуска:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

<b>Техническая информация:</b>
• Python 3.8+
• aiogram 2.25.2
• SQLite + Peewee ORM
• APScheduler для задач
"""
        
        await message.answer(
            version_text,
            parse_mode=ParseMode.HTML
        )


# Регистрация обработчика
@dp.message_handler(commands=['version'], chat_type='private')
async def version_cmd(message: types.Message):
    await VersionCommand.handle(message)
