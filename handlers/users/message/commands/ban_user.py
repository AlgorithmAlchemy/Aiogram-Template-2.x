from aiogram import types
from aiogram.types import ParseMode
import logging

from data.config import config
from loader import dp
from models.user import User
from filters.admin_filter import AdminFilter

logger = logging.getLogger(__name__)


class BanUserCommand:
    """Обработчик команды /ban_user"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /ban_user"""
        if message.from_user.id not in config.admin.owner_ids:
            await message.answer("❌ У вас нет прав администратора!")
            return
        
        # Проверяем, есть ли аргументы
        args = message.get_args().split()
        if not args:
            await message.answer(
                "🚫 <b>Бан пользователя</b>\n\n"
                "Использование: <code>/ban_user [ID/username] [причина]</code>\n\n"
                "Примеры:\n"
                "<code>/ban_user 123456789</code>\n"
                "<code>/ban_user @username</code>\n"
                "<code>/ban_user 123456789 Нарушение правил</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        target = args[0]
        reason = " ".join(args[1:]) if len(args) > 1 else "Причина не указана"
        
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
            
            # Проверяем, не пытается ли админ забанить сам себя
            if user_id == message.from_user.id:
                await message.answer("❌ Вы не можете забанить сами себя!")
                return
            
            # Проверяем, не пытается ли админ забанить другого админа
            if user_id in config.admin.owner_ids:
                await message.answer("❌ Вы не можете забанить другого администратора!")
                return
            
            # Баним пользователя
            user.ban()
            
            # Логируем действие
            logger.info(
                f"Admin {message.from_user.id} banned user {user_id}. "
                f"Reason: {reason}"
            )
            
            await message.answer(
                f"✅ <b>Пользователь забанен</b>\n\n"
                f"<b>ID:</b> <code>{user_id}</code>\n"
                f"<b>Имя:</b> {user.first_name}\n"
                f"<b>Username:</b> @{user.username or 'Не указан'}\n"
                f"<b>Причина:</b> {reason}\n"
                f"<b>Забанил:</b> {message.from_user.first_name}",
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error banning user {target}: {e}")
            await message.answer("❌ Произошла ошибка при бане пользователя!")


# Регистрация обработчика
@dp.message_handler(AdminFilter(), commands=['ban_user'])
async def ban_user_cmd(message: types.Message):
    await BanUserCommand.handle(message)
