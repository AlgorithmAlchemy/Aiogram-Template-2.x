"""
Команда /weather с использованием API wrapper
"""
from aiogram import types

from api.weather import WeatherAPIWrapper
from data.config import config
from loader import dp
from models.user import User


class WeatherCommand:
    """Команда получения погоды"""

    @staticmethod
    @dp.message_handler(commands=['weather'])
    async def handle(message: types.Message):
        """Обработчик команды /weather"""
        # Проверяем, есть ли API ключ
        if not hasattr(config, 'weather_api_key') or not config.weather_api_key:
            await message.answer(
                "❌ Сервис погоды временно недоступен.\n"
                "Обратитесь к администратору."
            )
            return

        # Получаем город из сообщения
        args = message.get_args()
        if not args:
            await message.answer(
                "🌤 <b>Прогноз погоды</b>\n\n"
                "Использование: <code>/weather [город]</code>\n\n"
                "Примеры:\n"
                "• <code>/weather Москва</code>\n"
                "• <code>/weather London</code>\n"
                "• <code>/weather New York</code>",
                parse_mode='HTML'
            )
            return

        city = args.strip()

        # Отправляем сообщение о загрузке
        loading_msg = await message.answer(
            f"🌤 Получаю прогноз погоды для <b>{city}</b>...",
            parse_mode='HTML'
        )

        try:
            # Создаем экземпляр API wrapper
            weather_api = WeatherAPIWrapper(api_key=config.weather_api_key)

            # Получаем данные о погоде
            weather_data = await weather_api.get_weather(city)

            if weather_data:
                # Формируем ответ
                response = f"""
🌤 <b>Прогноз погоды для {city}</b>

🌡 <b>Температура:</b> {weather_data.get('temp', 'N/A')}°C
🌡 <b>Ощущается как:</b> {weather_data.get('feels_like', 'N/A')}°C
💨 <b>Ветер:</b> {weather_data.get('wind_speed', 'N/A')} м/с
💧 <b>Влажность:</b> {weather_data.get('humidity', 'N/A')}%
☁️ <b>Облачность:</b> {weather_data.get('description', 'N/A')}

📅 <b>Обновлено:</b> {weather_data.get('updated_at', 'N/A')}
"""

                # Обновляем сообщение
                await loading_msg.edit_text(response, parse_mode='HTML')

                # Обновляем статистику пользователя
                try:
                    user = User.get(User.user_id == message.from_user.id)
                    user.update_activity()
                except Exception as e:
                    print(f"Error updating user activity: {e}")

            else:
                await loading_msg.edit_text(
                    f"❌ Не удалось получить прогноз погоды для <b>{city}</b>.\n"
                    "Проверьте правильность названия города.",
                    parse_mode='HTML'
                )

        except Exception as e:
            await loading_msg.edit_text(
                f"❌ Ошибка при получении прогноза погоды:\n<code>{str(e)}</code>",
                parse_mode='HTML'
            )

    @staticmethod
    @dp.message_handler(commands=['weather_help'])
    async def help_handler(message: types.Message):
        """Справка по команде weather"""
        help_text = """
🌤 <b>Справка по команде /weather</b>

<b>Описание:</b>
Получение текущего прогноза погоды для указанного города.

<b>Синтаксис:</b>
<code>/weather [город]</code>

<b>Примеры:</b>
• <code>/weather Москва</code>
• <code>/weather Санкт-Петербург</code>
• <code>/weather London</code>
• <code>/weather New York</code>

<b>Поддерживаемые форматы:</b>
• Название города на русском языке
• Название города на английском языке
• Название города с указанием страны

<b>Примечание:</b>
Данные предоставляются сервисом OpenWeatherMap.
"""

        await message.answer(help_text, parse_mode='HTML')
