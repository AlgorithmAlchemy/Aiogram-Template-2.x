import logging

from aiogram import types
from aiogram.types import ParseMode

from app.data.config import config
from app.keyboards.inline.keyboards import UtilityKeyboards
from app.loader import dp

logger = logging.getLogger(__name__)


class SupportCommand:
    """Обработчик команды /support"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /support - связаться с поддержкой"""
        support_text = f"""
<b>🆘 Поддержка</b>

Нужна помощь? Мы готовы помочь!

<b>Способы связи:</b>
• <b>Поддержка:</b> {config.bot.support}
• <b>Чат:</b> {config.chat_id}
• <b>Владелец:</b> {config.bot.owner}

<b>Что мы можем помочь:</b>
• Настройка бота
• Решение проблем
• Добавление функций
• Общие вопросы

<b>Время работы:</b> 24/7

<i>Не стесняйтесь обращаться!</i>
"""

        await message.answer(
            support_text,
            parse_mode=ParseMode.HTML,
            reply_markup=UtilityKeyboards.get_back_keyboard()
        )


# Регистрация обработчика
@dp.message_handler(commands=['support'], chat_type='private')
async def support_cmd(message: types.Message):
    await SupportCommand.handle(message)
