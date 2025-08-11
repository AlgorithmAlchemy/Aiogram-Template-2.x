from aiogram import types
from aiogram.types import ParseMode
import logging

from data.config import config
from loader import dp
from models.user import User
from filters.admin_filter import AdminFilter

logger = logging.getLogger(__name__)


class UnbanUserCommand:
    """Обработчик команды /unban_user"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /unban_user"""
        if message.from_user.id not in config.admin.owner_ids:
            await message.answer("❌ У вас нет прав администратора!")
            return
        
        # Проверяем, есть ли аргументы
        args = message.get_args().split()
        if not args:
            await message.answer(
                "✅ <b>Разбан пользователя</b>\n\n"
                "Использование: <code>/unban_user [ID/username]</code>\n\n"
                "Примеры:\n"
                "<code>/unban_user 123456789</code>\n"
                "<code>/unban_user @username</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        target = args[0]
        
        try:
            # Определяем ID пользователя
            if target.startswith('@'):
                # По username
                username = target[1:]
                user = User.get_or_none(User.username == username)
                if not user:
                    await message.answer(
                        f"❌ Пользователь @{username} не найден в базе данных!"
                    )
                    return
                user_id = user.user_id
            else:
                # По ID
                try:
                    user_id = int(target)
                except ValueError:
                    await message.answer("❌ Неверный формат ID пользователя!")
                    return
                
                user = User.get_or_none(User.user_id == user_id)
                if not user:
                    await message.answer(
                        f"❌ Пользователь с ID {user_id} не найден в базе данных!"
                    )
                    return
            
            # Проверяем, забанен ли пользователь
            if not user.is_banned:
                await message.answer("❌ Пользователь не забанен!")
                return
            
            # Разбаниваем пользователя
            user.unban()
            
            # Логируем действие
            logger.info(
                f"Admin {message.from_user.id} unbanned user {user_id}"
            )
            
            await message.answer(
                f"✅ <b>Пользователь разбанен</b>\n\n"
                f"<b>ID:</b> <code>{user_id}</code>\n"
                f"<b>Имя:</b> {user.first_name}\n"
                f"<b>Username:</b> @{user.username or 'Не указан'}\n"
                f"<b>Разбанил:</b> {message.from_user.first_name}",
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error unbanning user {target}: {e}")
            await message.answer("❌ Произошла ошибка при разбане пользователя!")


# Регистрация обработчика
@dp.message_handler(AdminFilter(), commands=['unban_user'])
async def unban_user_cmd(message: types.Message):
    await UnbanUserCommand.handle(message)
