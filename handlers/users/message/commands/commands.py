import logging

from aiogram import types
from aiogram.types import ParseMode

from data.config import config
from keyboards.inline.keyboards import UtilityKeyboards
from loader import dp

logger = logging.getLogger(__name__)


class CommandsCommand:
    """Обработчик команды /commands"""

    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /commands - показывает все команды"""
        commands_text = f"""
<b>📋 Доступные команды</b>

<b>Основные команды:</b>
/start - Запустить бота и показать главное меню
/menu - Показать главное меню
/help - Показать справку
/about - Информация о боте
/commands - Показать все команды

<b>Пользовательские команды:</b>
/profile - Показать ваш профиль
/settings - Открыть настройки
/feedback - Отправить отзыв
/support - Связаться с поддержкой

<b>Информационные команды:</b>
/version - Версия бота
/status - Статус бота
/ping - Проверить соединение
/uptime - Время работы бота

<b>Админские команды:</b>
/ban_user - Забанить пользователя
/unban_user - Разбанить пользователя
/warn_user - Предупредить пользователя
/stats - Статистика бота
/users - Список пользователей

<b>Поддержка:</b> {config.bot.support}
"""

        await message.answer(
            commands_text,
            parse_mode=ParseMode.HTML,
            reply_markup=UtilityKeyboards.get_back_keyboard()
        )


# Регистрация обработчика
@dp.message_handler(commands=['commands'], chat_type='private')
async def commands_cmd(message: types.Message):
    await CommandsCommand.handle(message)
