"""
Примеры использования всех компонентов шаблона

Этот файл демонстрирует, как использовать различные возможности шаблона:
- FSM состояния
- API wrappers
- Middleware
- Event hooks
- Команды
"""

import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import config
from models.user import User, UserSettings, UserStats
from api.weather import WeatherAPIWrapper
from api.currency import CurrencyAPIWrapper
from utils.hooks.event_hooks import EventHooks
from keyboards.inline.keyboards import MainKeyboards, AdminKeyboards


# ============================================================================
# ПРИМЕР 1: Использование FSM состояний
# ============================================================================

async def example_fsm_usage():
    """
    Пример использования FSM для многошагового диалога
    """
    print("=== Пример FSM использования ===")
    
    # В реальном обработчике это выглядело бы так:
    """
    @dp.message_handler(commands=['survey'])
    async def start_survey(message: types.Message, state: FSMContext):
        await state.set_state('waiting_for_age')
        await message.answer("Сколько вам лет?")
    
    @dp.message_handler(state='waiting_for_age')
    async def process_age(message: types.Message, state: FSMContext):
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state('waiting_for_city')
        await message.answer("В каком городе вы живете?")
    
    @dp.message_handler(state='waiting_for_city')
    async def process_city(message: types.Message, state: FSMContext):
        city = message.text
        data = await state.get_data()
        await state.finish()
        await message.answer(f"Спасибо! Вам {data['age']} лет, вы из {city}")
    """


# ============================================================================
# ПРИМЕР 2: Использование API wrappers
# ============================================================================

async def example_api_wrappers():
    """
    Пример использования API wrappers
    """
    print("=== Пример API wrappers ===")
    
    # Weather API
    if hasattr(config, 'weather_api_key') and config.weather_api_key:
        weather_api = WeatherAPIWrapper(api_key=config.weather_api_key)
        weather_data = await weather_api.get_weather("Москва")
        print(f"Weather data: {weather_data}")
    
    # Currency API
    if hasattr(config, 'currency_api_key') and config.currency_api_key:
        currency_api = CurrencyAPIWrapper(api_key=config.currency_api_key)
        rate = await currency_api.get_exchange_rate("USD", "RUB")
        print(f"Exchange rate: {rate}")


# ============================================================================
# ПРИМЕР 3: Работа с базой данных
# ============================================================================

def example_database_usage():
    """
    Пример работы с базой данных
    """
    print("=== Пример работы с БД ===")
    
    # Создание пользователя
    user, created = User.get_or_create(
        user_id=123456789,
        defaults={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe'
        }
    )
    
    if created:
        print(f"Создан новый пользователь: {user}")
    else:
        print(f"Пользователь уже существует: {user}")
    
    # Обновление статистики
    stats, _ = UserStats.get_or_create(user=user)
    stats.increment_messages()
    stats.increment_commands()
    print(f"Статистика обновлена: {stats}")
    
    # Получение настроек
    settings, _ = UserSettings.get_or_create(user=user)
    settings.language = 'en'
    settings.save()
    print(f"Настройки обновлены: {settings}")


# ============================================================================
# ПРИМЕР 4: Использование Event Hooks
# ============================================================================

def example_event_hooks():
    """
    Пример использования event hooks
    """
    print("=== Пример Event Hooks ===")
    
    event_hooks = EventHooks()
    
    # Регистрация startup hook
    @event_hooks.startup_hook
    async def custom_startup():
        print("Custom startup hook executed")
    
    # Регистрация message hook
    @event_hooks.message_hook
    async def custom_message_hook(message: types.Message):
        print(f"Message hook: {message.text}")
    
    # Регистрация error hook
    @event_hooks.error_hook
    async def custom_error_hook(update, exception):
        print(f"Error hook: {exception}")
    
    return event_hooks


# ============================================================================
# ПРИМЕР 5: Создание клавиатур
# ============================================================================

def example_keyboards():
    """
    Пример создания клавиатур
    """
    print("=== Пример клавиатур ===")
    
    # Главное меню
    main_menu = MainKeyboards.get_main_menu()
    print(f"Main menu keyboard: {main_menu}")
    
    # Админ панель
    admin_panel = AdminKeyboards.get_admin_panel()
    print(f"Admin panel keyboard: {admin_panel}")
    
    # Кастомная клавиатура
    custom_kb = MainKeyboards.create_keyboard([
        [("Кнопка 1", "btn1"), ("Кнопка 2", "btn2")],
        [("Кнопка 3", "btn3")]
    ])
    print(f"Custom keyboard: {custom_kb}")


# ============================================================================
# ПРИМЕР 6: Middleware
# ============================================================================

def example_middleware():
    """
    Пример создания middleware
    """
    print("=== Пример Middleware ===")
    
    from utils.middleware.custom_middleware import LoggingMiddleware
    
    # Создание middleware
    logging_middleware = LoggingMiddleware()
    print(f"Logging middleware created: {logging_middleware}")
    
    # В реальном коде middleware регистрируется так:
    """
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(AdminMiddleware())
    """


# ============================================================================
# ПРИМЕР 7: Команды с параметрами
# ============================================================================

async def example_commands():
    """
    Пример создания команд с параметрами
    """
    print("=== Пример команд ===")
    
    # Команда с аргументами
    """
    @dp.message_handler(commands=['search'])
    async def search_command(message: types.Message):
        args = message.get_args()
        if not args:
            await message.answer("Использование: /search [запрос]")
            return
        
        query = args.strip()
        # Выполнение поиска
        results = await perform_search(query)
        await message.answer(f"Результаты поиска для '{query}': {results}")
    """
    
    # Команда с inline клавиатурой
    """
    @dp.message_handler(commands=['menu'])
    async def menu_command(message: types.Message):
        keyboard = MainKeyboards.get_main_menu()
        await message.answer("Выберите действие:", reply_markup=keyboard)
    """


# ============================================================================
# ПРИМЕР 8: Обработка callback queries
# ============================================================================

async def example_callback_handlers():
    """
    Пример обработки callback queries
    """
    print("=== Пример callback handlers ===")
    
    """
    @dp.callback_query_handler(lambda c: c.data.startswith('btn_'))
    async def process_callback(callback_query: types.CallbackQuery):
        await callback_query.answer()
        
        if callback_query.data == 'btn_profile':
            user = User.get(User.user_id == callback_query.from_user.id)
            await callback_query.message.edit_text(
                f"Профиль: {user.first_name} {user.last_name}"
            )
        elif callback_query.data == 'btn_settings':
            await callback_query.message.edit_text("Настройки бота")
    """


# ============================================================================
# ПРИМЕР 9: Планировщик задач
# ============================================================================

def example_scheduler():
    """
    Пример использования планировщика
    """
    print("=== Пример планировщика ===")
    
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    
    scheduler = AsyncIOScheduler()
    
    # Ежедневная задача в 9:00
    """
    async def daily_task():
        print("Выполняется ежедневная задача")
        # Отправка статистики администраторам
        # Очистка старых данных
        # Резервное копирование
    
    scheduler.add_job(
        daily_task,
        trigger=CronTrigger(hour=9, minute=0),
        id='daily_task'
    )
    """
    
    print("Scheduler example created")


# ============================================================================
# ПРИМЕР 10: Обработка ошибок
# ============================================================================

async def example_error_handling():
    """
    Пример обработки ошибок
    """
    print("=== Пример обработки ошибок ===")
    
    """
    @dp.errors_handler()
    async def errors_handler(update, exception):
        logger.error(f"Update {update} caused error {exception}")
        
        # Отправка уведомления администратору
        for admin_id in config.admin.owner_ids:
            try:
                await bot.send_message(
                    admin_id,
                    f"Ошибка в боте: {exception}"
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
        
        return True
    """


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ДЛЯ ДЕМОНСТРАЦИИ
# ============================================================================

async def demonstrate_all_features():
    """
    Демонстрация всех возможностей шаблона
    """
    print("🚀 Демонстрация возможностей aiogram 2.x шаблона")
    print("=" * 60)
    
    # 1. Работа с БД
    example_database_usage()
    print()
    
    # 2. Event hooks
    example_event_hooks()
    print()
    
    # 3. Клавиатуры
    example_keyboards()
    print()
    
    # 4. Middleware
    example_middleware()
    print()
    
    # 5. Планировщик
    example_scheduler()
    print()
    
    # 6. API wrappers (если есть ключи)
    await example_api_wrappers()
    print()
    
    # 7. FSM
    await example_fsm_usage()
    print()
    
    print("✅ Демонстрация завершена!")
    print("\n📚 Для получения дополнительной информации:")
    print("• README.md - основная документация")
    print("• examples/ - дополнительные примеры")
    print("• handlers/ - примеры обработчиков")


if __name__ == "__main__":
    # Запуск демонстрации
    asyncio.run(demonstrate_all_features())
