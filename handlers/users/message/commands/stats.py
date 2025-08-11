from aiogram import types
from aiogram.types import ParseMode
import logging
from datetime import datetime, timedelta

from data.config import config
from loader import dp
from models.user import User, UserStats
from filters.admin_filter import AdminFilter

logger = logging.getLogger(__name__)


class StatsCommand:
    """Обработчик команды /stats"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /stats - статистика бота"""
        if message.from_user.id not in config.admin.owner_ids:
            await message.answer("❌ У вас нет прав администратора!")
            return
        
        try:
            # Получаем статистику
            total_users = User.select().count()
            active_today = User.select().where(
                User.last_activity >= datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            ).count()
            active_week = User.select().where(
                User.last_activity >= datetime.now() - timedelta(days=7)
            ).count()
            banned_users = User.select().where(User.is_banned).count()
            
            # Получаем общую статистику сообщений
            total_messages = sum(
                stats.messages_sent for stats in UserStats.select()
            )
            total_commands = sum(
                stats.commands_used for stats in UserStats.select()
            )
            total_files = sum(
                stats.files_sent for stats in UserStats.select()
            )
            
            stats_text = f"""
<b>📊 Статистика бота</b>

<b>Пользователи:</b>
• Всего пользователей: {total_users}
• Активных сегодня: {active_today}
• Активных за неделю: {active_week}
• Забаненных: {banned_users}

<b>Активность:</b>
• Всего сообщений: {total_messages}
• Всего команд: {total_commands}
• Всего файлов: {total_files}

<b>Система:</b>
• Версия бота: {config.bot.version}
• Время работы: {StatsCommand._get_uptime()}
• Статус: ✅ Активен

<b>Обновлено:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""
            
            await message.answer(
                stats_text,
                parse_mode=ParseMode.HTML
            )
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            await message.answer("❌ Ошибка при получении статистики")
    
    @staticmethod
    def _get_uptime() -> str:
        """Возвращает время работы бота"""
        return "Неизвестно"


# Регистрация обработчика
@dp.message_handler(AdminFilter(), commands=['stats'])
async def stats_cmd(message: types.Message):
    await StatsCommand.handle(message)
