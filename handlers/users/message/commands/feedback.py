import logging

from aiogram import types
from aiogram.types import ParseMode

from data.config import config
from keyboards.inline.keyboards import UtilityKeyboards
from loader import dp

logger = logging.getLogger(__name__)


class FeedbackCommand:
    """Обработчик команды /feedback"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /feedback - отправить отзыв"""
        feedback_text = f"""
<b>📝 Отправить отзыв</b>

Мы ценим ваше мнение! Поделитесь своими впечатлениями о боте.

<b>Как отправить отзыв:</b>
1. Напишите ваше сообщение
2. Мы получим его и рассмотрим
3. При необходимости свяжемся с вами

<b>Что можно написать:</b>
• Предложения по улучшению
• Сообщения об ошибках
• Общие впечатления
• Пожелания по функционалу

<b>Поддержка:</b> {config.bot.support}

<i>Просто напишите ваше сообщение в следующем сообщении.</i>
"""

        await message.answer(
            feedback_text,
            parse_mode=ParseMode.HTML,
            reply_markup=UtilityKeyboards.get_back_keyboard()
        )


# Регистрация обработчика
@dp.message_handler(commands=['feedback'], chat_type='private')
async def feedback_cmd(message: types.Message):
    await FeedbackCommand.handle(message)
