import logging

from aiogram import types
from aiogram.types import ParseMode

from data.config import config
from handlers.base_handler import BaseCommandHandler
from loader import dp
from models.user import User

logger = logging.getLogger(__name__)


class BanUserCommandHandler(BaseCommandHandler):
    """Обработчик команды /ban_user"""

    def get_command(self) -> str:
        return "ban_user"

    async def handle(self, message: types.Message):
        """Обработчик команды /ban_user"""
        if message.from_user.id not in config.admin.owner_ids:
            await message.answer("❌ У вас нет прав администратора!")
            return

        # Получаем аргументы команды
        args = message.get_args().split()
        if not args:
            await message.answer(
                "❌ Укажите ID или username пользователя!\n"
                "Пример: /ban_user 123456789 или /ban_user @username"
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
                await message.answer(
                    "❌ Вы не можете забанить другого администратора!"
                )
                return

            # Проверяем, не забанен ли уже пользователь
            if user.is_banned:
                await message.answer("❌ Пользователь уже заблокирован!")
                return

            # Баним пользователя
            user.ban()

            # Логируем действие
            logger.info(
                f"Admin {message.from_user.id} banned user {user_id} "
                f"for reason: {reason}"
            )

            # Отправляем подтверждение
            ban_text = f"""
<b>🚫 Пользователь заблокирован</b>

<b>ID:</b> <code>{user_id}</code>
<b>Имя:</b> {user.first_name}
<b>Username:</b> @{user.username or 'Не указан'}
<b>Причина:</b> {reason}
<b>Администратор:</b> {message.from_user.first_name}

<i>Пользователь больше не сможет использовать бота</i>
"""

            await message.answer(
                ban_text,
                parse_mode=ParseMode.HTML
            )

        except Exception as e:
            logger.error(f"Error banning user: {e}")
            await message.answer("❌ Ошибка при блокировке пользователя")


# Создаем экземпляр хэндлера для автоматической регистрации
ban_user_handler = BanUserCommandHandler(dp)
