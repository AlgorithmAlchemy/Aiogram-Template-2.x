import logging

from aiogram import types
from aiogram.types import ParseMode

from app.keyboards.inline.keyboards import MainKeyboards
from app.loader import dp

logger = logging.getLogger(__name__)


class SettingsCommand:
    """Обработчик команды /settings"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /settings - открыть настройки"""
        settings_text = """
<b>⚙️ Настройки</b>

Здесь вы можете настроить различные параметры бота:

• <b>Язык интерфейса</b> - выбрать язык бота
• <b>Уведомления</b> - настройка уведомлений
• <b>Тема</b> - выбор темы оформления
• <b>Приватность</b> - настройки приватности

<i>Настройки будут доступны в следующем обновлении.</i>
"""

        await message.answer(
            settings_text,
            parse_mode=ParseMode.HTML,
            reply_markup=MainKeyboards.get_settings_keyboard()
        )


# Регистрация обработчика
@dp.message_handler(commands=['settings'], chat_type='private')
async def settings_cmd(message: types.Message):
    await SettingsCommand.handle(message)
