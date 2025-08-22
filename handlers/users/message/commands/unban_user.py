from aiogram import types
from aiogram.types import ParseMode
import logging

from data.config import config
from loader import dp
from models.user import User

logger = logging.getLogger(__name__)


class UnbanUserCommand:
    """Обработчик команды /unban_user"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /unban_user"""
        if message.from_user.id not in config.admin.owner_ids:
            await message.answer("❌ У вас нет прав администратора!")
            return
        
        # Получаем аргументы команды
        args = message.get_args().split()
        if not args:
            await message.answer(
                "❌ Укажите ID или username пользователя!\n"
                "Пример: /unban_user 123456789 или /unban_user @username"
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
            
            # Проверяем, не пытается ли админ разбанить сам себя
            if user_id == message.from_user.id:
                await message.answer("❌ Вы не можете разбанить сами себя!")
                return
            
            # Проверяем, не забанен ли пользователь
            if not user.is_banned:
                await message.answer("❌ Пользователь не заблокирован!")
                return
            
            # Разбаниваем пользователя
            user.unban()
            
            # Логируем действие
            logger.info(
                f"Admin {message.from_user.id} unbanned user {user_id}"
            )
            
            # Отправляем подтверждение
            unban_text = f"""
<b>✅ Пользователь разблокирован</b>

<b>ID:</b> <code>{user_id}</code>
<b>Имя:</b> {user.first_name}
<b>Username:</b> @{user.username or 'Не указан'}
<b>Администратор:</b> {message.from_user.first_name}

<i>Пользователь снова может использовать бота</i>
"""
            
            await message.answer(
                unban_text,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error unbanning user: {e}")
            await message.answer("❌ Ошибка при разблокировке пользователя")


# Регистрация обработчика
@dp.message_handler(commands=['unban_user'], chat_type='private')
async def unban_user_cmd(message: types.Message):
    await UnbanUserCommand.handle(message)
