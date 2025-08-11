from aiogram import types
from aiogram.types import ParseMode
import logging
import time

from loader import dp

logger = logging.getLogger(__name__)


class PingCommand:
    """Обработчик команды /ping"""
    
    @staticmethod
    async def handle(message: types.Message):
        """Обработчик команды /ping - проверка соединения"""
        start_time = time.time()
        
        # Отправляем сообщение и измеряем время
        sent_message = await message.answer("🏓 Pong!")
        end_time = time.time()
        
        # Вычисляем задержку
        latency = round((end_time - start_time) * 1000, 2)
        
        # Обновляем сообщение с информацией о задержке
        await sent_message.edit_text(
            f"🏓 <b>Pong!</b>\n\n"
            f"<b>Задержка:</b> {latency}ms\n"
            f"<b>Статус:</b> ✅ Соединение активно",
            parse_mode=ParseMode.HTML
        )


# Регистрация обработчика
@dp.message_handler(commands=['ping'], chat_type='private')
async def ping_cmd(message: types.Message):
    await PingCommand.handle(message)
