from aiogram import types
from aiogram.types import ParseMode
import logging

from data.config import config
from loader import dp
from models.user import User
from handlers.base_handler import BaseCommandHandler

logger = logging.getLogger(__name__)


class WarnUserCommandHandler(BaseCommandHandler):
    """Обработчик команды /warn_user"""
    
    def get_command(self) -> str:
        return "warn_user"
    
    async def handle(self, message: types.Message):
        """Обработчик команды /warn_user"""
        if message.from_user.id not in config.admin.owner_ids:
            await message.answer("❌ У вас нет прав администратора!")
            return
        
        # Получаем аргументы команды
        args = message.get_args().split()
        if not args:
            await message.answer(
                "❌ Укажите ID или username пользователя!\n"
                "Пример: /warn_user 123456789 или /warn_user @username"
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
            
            # Проверяем, не пытается ли админ предупредить сам себя
            if user_id == message.from_user.id:
                await message.answer("❌ Вы не можете предупредить сами себя!")
                return
            
            # Проверяем, не забанен ли пользователь
            if user.is_banned:
                await message.answer("❌ Пользователь заблокирован!")
                return
            
            # Проверяем, можно ли добавить предупреждение
            if not user.can_be_warned():
                await message.answer(
                    f"❌ Пользователь уже имеет максимальное количество "
                    f"предупреждений ({user.warnings}/{user.max_warnings})!"
                )
                return
            
            # Добавляем предупреждение
            user.add_warning()
            
            # Логируем действие
            logger.info(
                f"Admin {message.from_user.id} warned user {user_id} "
                f"for reason: {reason}"
            )
            
            # Отправляем подтверждение
            warn_text = f"""
<b>⚠️ Пользователь предупрежден</b>

<b>ID:</b> <code>{user_id}</code>
<b>Имя:</b> {user.first_name}
<b>Username:</b> @{user.username or 'Не указан'}
<b>Причина:</b> {reason}
<b>Администратор:</b> {message.from_user.first_name}

<b>Предупреждения:</b> {user.warnings}/{user.max_warnings}

<i>При достижении максимума предупреждений пользователь будет заблокирован</i>
"""
            
            await message.answer(
                warn_text,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error warning user: {e}")
            await message.answer("❌ Ошибка при предупреждении пользователя")


# Создаем экземпляр хэндлера для автоматической регистрации
warn_user_handler = WarnUserCommandHandler(dp)
