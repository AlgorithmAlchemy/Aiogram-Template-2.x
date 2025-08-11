from aiogram import types
from aiogram.types import ParseMode
import logging

from data.config import config
from loader import dp
from keyboards.inline.keyboards import MainKeyboards

logger = logging.getLogger(__name__)


class MenuCommand:
    """Обработчик команды /menu"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /menu - показывает главное меню"""
        user_id = message.from_user.id
        
        if user_id in config.admin.owner_ids:
            await message.answer(
                "🔧 <b>Панель администратора</b>\n\nВыберите действие:",
                parse_mode=ParseMode.HTML,
                reply_markup=MainKeyboards.get_admin_keyboard()
            )
        else:
            await message.answer(
                "🏠 <b>Главное меню</b>\n\nВыберите действие:",
                parse_mode=ParseMode.HTML,
                reply_markup=MainKeyboards.get_main_keyboard()
            )


# Регистрация обработчика
@dp.message_handler(commands=['menu'], chat_type='private')
async def menu_cmd(message: types.Message):
    await MenuCommand.handle(message)
