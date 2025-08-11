# 📚 Примеры использования Aiogram 2.x Template

Этот файл содержит примеры и шаблоны для работы с данным проектом.

## 🎯 Основные примеры

### 1. Создание простого обработчика команды

```python
# handlers/users/message/example.py
from aiogram import types
from aiogram.types import ParseMode
from loader import dp

@dp.message_handler(commands=['example'])
async def example_command(message: types.Message):
    """Пример простого обработчика команды"""
    await message.answer(
        "Это пример обработчика команды!",
        parse_mode=ParseMode.HTML
    )
```

### 2. Создание inline клавиатуры

```python
# keyboards/inline/keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_example_keyboard() -> InlineKeyboardMarkup:
    """Пример создания inline клавиатуры"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("Кнопка 1", callback_data="btn_1"),
        InlineKeyboardButton("Кнопка 2", callback_data="btn_2")
    )
    keyboard.add(
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )
    
    return keyboard
```

### 3. Обработка callback кнопок

```python
# handlers/users/callback/example.py
from aiogram import types
from loader import dp

@dp.callback_query_handler(lambda c: c.data == "btn_1")
async def button_1_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 1"""
    await callback_query.answer("Вы нажали кнопку 1!")
    await callback_query.message.edit_text(
        "Содержимое кнопки 1",
        reply_markup=get_back_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == "btn_2")
async def button_2_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 2"""
    await callback_query.answer("Вы нажали кнопку 2!")
    await callback_query.message.edit_text(
        "Содержимое кнопки 2",
        reply_markup=get_back_keyboard()
    )
```

### 4. Работа с FSM (машины состояний)

```python
# states/example_states.py
from aiogram.dispatcher.filters.state import State, StatesGroup

class ExampleStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_confirm = State()

# handlers/users/message/example_fsm.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.example_states import ExampleStates
from keyboards.inline.keyboards import get_confirm_keyboard

@dp.message_handler(commands=['register'])
async def start_registration(message: types.Message):
    """Начало регистрации"""
    await message.answer("Введите ваше имя:")
    await ExampleStates.waiting_for_name.set()

@dp.message_handler(state=ExampleStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    """Обработка имени"""
    async with state.proxy() as data:
        data['name'] = message.text
    
    await message.answer("Введите ваш возраст:")
    await ExampleStates.waiting_for_age.set()

@dp.message_handler(state=ExampleStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    """Обработка возраста"""
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом! Попробуйте снова:")
        return
    
    async with state.proxy() as data:
        data['age'] = int(message.text)
    
    await message.answer(
        f"Подтвердите данные:\nИмя: {data['name']}\nВозраст: {data['age']}",
        reply_markup=get_confirm_keyboard("registration")
    )
    await ExampleStates.waiting_for_confirm.set()

@dp.callback_query_handler(lambda c: c.data == "confirm_registration", 
                          state=ExampleStates.waiting_for_confirm)
async def confirm_registration(callback_query: types.CallbackQuery, state: FSMContext):
    """Подтверждение регистрации"""
    async with state.proxy() as data:
        name = data['name']
        age = data['age']
    
    # Здесь можно сохранить данные в базу
    await callback_query.message.edit_text(
        f"Регистрация завершена!\nИмя: {name}\nВозраст: {age}"
    )
    await state.finish()
```

### 5. Создание модели базы данных

```python
# models/user.py
from peewee import *
from utils.db_api.sqlite import db

class User(Model):
    """Модель пользователя"""
    user_id = IntegerField(unique=True)
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)
    
    class Meta:
        database = db
        table_name = 'users'

# Создание таблицы
User.create_table()
```

### 6. Работа с базой данных

```python
# handlers/users/message/database_example.py
from aiogram import types
from loader import dp
from models.user import User

@dp.message_handler(commands=['save_user'])
async def save_user_command(message: types.Message):
    """Сохранение пользователя в базу данных"""
    user = message.from_user
    
    # Проверяем, существует ли пользователь
    existing_user = User.get_or_none(User.user_id == user.id)
    
    if existing_user:
        await message.answer("Пользователь уже существует в базе!")
        return
    
    # Создаем нового пользователя
    new_user = User.create(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    await message.answer(f"Пользователь {new_user.first_name} сохранен в базе!")

@dp.message_handler(commands=['get_users'])
async def get_users_command(message: types.Message):
    """Получение списка пользователей"""
    users = User.select()
    user_list = "\n".join([f"• {user.first_name} (@{user.username})" for user in users])
    
    await message.answer(f"Список пользователей:\n{user_list}")
```

### 7. Создание фильтра

```python
# filters/admin_filter.py
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import OWNER

class AdminFilter(BoundFilter):
    """Фильтр для проверки администратора"""
    
    async def check(self, message: types.Message):
        return message.from_user.id in OWNER

# Регистрация фильтра в loader.py
# dp.filters_factory.bind(AdminFilter)
```

### 8. Использование фильтра

```python
# handlers/users/message/admin_commands.py
from aiogram import types
from loader import dp
from filters.admin_filter import AdminFilter

@dp.message_handler(AdminFilter(), commands=['admin_only'])
async def admin_only_command(message: types.Message):
    """Команда только для администраторов"""
    await message.answer("Эта команда доступна только администраторам!")
```

### 9. Планировщик задач

```python
# utils/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from data.config import TIMEZONE

scheduler = AsyncIOScheduler(timezone=TIMEZONE)

async def send_daily_message():
    """Отправка ежедневного сообщения"""
    # Здесь можно отправить сообщение всем пользователям
    pass

# Добавление задачи в main.py
# scheduler.add_job(send_daily_message, trigger='cron', hour=9, minute=0)
```

### 10. Обработка ошибок

```python
# handlers/errors/message/error_handler.py
from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
from loader import dp

@dp.errors_handler()
async def errors_handler(update, exception):
    """Глобальный обработчик ошибок"""
    if isinstance(exception, TelegramAPIError):
        # Обработка ошибок Telegram API
        return True
    
    # Логирование других ошибок
    print(f"Unexpected error: {exception}")
    return True
```

## 🔧 Полезные утилиты

### Логирование

```python
import logging

logger = logging.getLogger(__name__)

# В обработчиках
logger.info("Пользователь выполнил действие")
logger.error("Произошла ошибка", exc_info=True)
logger.warning("Предупреждение")
```

### Валидация данных

```python
def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    import re
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Валидация email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Работа с файлами

```python
import os
from aiogram import types

@dp.message_handler(content_types=['document'])
async def handle_document(message: types.Message):
    """Обработка загруженных документов"""
    file = message.document
    
    # Создаем папку для файлов, если её нет
    os.makedirs('downloads', exist_ok=True)
    
    # Скачиваем файл
    file_path = f"downloads/{file.file_name}"
    await file.download(file_path)
    
    await message.answer(f"Файл {file.file_name} сохранен!")
```

## 🚀 Советы по разработке

1. **Всегда используйте типизацию** для лучшей читаемости кода
2. **Добавляйте docstrings** к функциям и классам
3. **Используйте логирование** для отладки
4. **Обрабатывайте исключения** для стабильности
5. **Следуйте структуре проекта** для организации кода
6. **Тестируйте код** перед деплоем
7. **Используйте переменные окружения** для конфигурации

## 📖 Дополнительные ресурсы

- [Документация aiogram 2.x](https://docs.aiogram.dev/en/v2/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Peewee ORM](http://docs.peewee-orm.com/)
- [APScheduler](https://apscheduler.readthedocs.io/)
