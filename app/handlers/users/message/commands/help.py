import logging

from aiogram import types
from aiogram.types import ParseMode

from app.data.config import config
from app.keyboards.inline.keyboards import UtilityKeyboards
from app.loader import dp

logger = logging.getLogger(__name__)


class HelpCommand:
    """Обработчик команды /help"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /help"""
        user_id = message.from_user.id

        # Проверяем, является ли пользователь администратором
        if user_id in config.admin.owner_ids:
            await message.answer(
                config.admin_help_text,
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(
                config.help_text,
                parse_mode=ParseMode.HTML,
                reply_markup=UtilityKeyboards.get_back_keyboard()
            )


# Регистрация обработчика
@dp.message_handler(commands=['help'], chat_type='private')
async def help_cmd(message: types.Message):
    await HelpCommand.handle(message)
