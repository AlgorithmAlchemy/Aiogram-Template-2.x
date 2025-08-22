# Архитектура проекта

## Обзор

Проект использует современную архитектуру с четким разделением ответственности:

- **main.py** - Единая точка входа и регистрации
- **ООП подход** для всех хэндлеров
- **Улучшенная архитектура БД** с миграциями
- **Модульная структура** без скрытых зависимостей

## Структура проекта

```
├── main.py                    # Главная точка входа
├── loader.py                  # Загрузка конфигурации
├── data/                      # Конфигурация и данные
├── models/                    # Модели базы данных
│   ├── base.py               # Базовая модель
│   ├── user.py               # Модели пользователей
│   ├── migrations.py         # Система миграций
│   └── sqlite3_creator.py    # Менеджер БД
├── database/                  # Подключение к БД
│   └── connection.py         # Настройки подключения
├── api/                       # Внешние API
│   ├── base.py               # Базовый класс API
│   ├── weather.py            # API погоды
│   └── currency.py           # API валют
├── handlers/                  # Обработчики
│   ├── base_handler.py       # Базовые классы хэндлеров
│   └── users/message/commands/ # Команды пользователей
├── middleware/                # Middleware
│   ├── base.py               # Базовый класс middleware
│   ├── logging.py            # Логирование
│   ├── throttling.py         # Ограничение частоты
│   ├── admin.py              # Проверка админов
│   └── database.py           # Работа с БД
├── utils/                     # Утилиты
├── filters/                   # Фильтры
├── states/                    # FSM состояния
├── keyboards/                 # Клавиатуры
└── examples/                  # Примеры использования
```

## Архитектура загрузки

### Loader (loader.py)

Базовый загрузчик для инициализации бота:

```python
class BotLoader:
    """Класс для базовой инициализации бота"""
    
    def setup_storage(self):
        """Настройка хранилища состояний"""
        # Memory или Redis storage
    
    def setup_bot(self):
        """Инициализация бота"""
        # Создание экземпляра бота
    
    def setup_dispatcher(self):
        """Инициализация диспетчера"""
        # Создание диспетчера
    
    def initialize(self):
        """Базовая инициализация"""
        # Возвращает bot, dp
```

### BotManager (main.py)

Центральный класс для управления жизненным циклом бота:

```python
class BotManager:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
    
    async def on_startup(self, dp: Dispatcher):
        """Действия при запуске"""
        # Подключение к БД
        # Регистрация хэндлеров
        # Настройка middleware
        # Регистрация фильтров
        # Настройка обработчиков ошибок
    
    async def on_shutdown(self, dp: Dispatcher):
        """Действия при остановке"""
        # Закрытие соединений
        # Очистка ресурсов
```

### Регистрация хэндлеров

Все хэндлеры регистрируются явно в main.py:

```python
async def register_handlers(self):
    """Регистрация всех хэндлеров"""
    
    # Импортируем хэндлеры
    from handlers.users.message.commands.start import StartCommandHandler
    from handlers.users.message.commands.profile import ProfileCommandHandler
    # ... другие импорты
    
    # Создаем экземпляры для автоматической регистрации
    handlers = [
        StartCommandHandler(self.dp),
        ProfileCommandHandler(self.dp),
        # ... другие хэндлеры
    ]
```

## Middleware

### Базовый класс

```python
class BaseCustomMiddleware(BaseMiddleware):
    """Базовый класс для всех middleware"""
    
    async def __call__(self, handler, event, data):
        start_time = time.time()
        
        try:
            # Предобработка
            await self.pre_process(event, data)
            
            # Выполнение обработчика
            result = await handler(event, data)
            
            # Постобработка
            await self.post_process(event, data, result)
            
            return result
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            raise
```

### Примеры middleware

```python
class LoggingMiddleware(BaseCustomMiddleware):
    """Middleware для логирования"""
    
    async def pre_process(self, event, data):
        logger.info(f"Message from {event.from_user.id}")

class AdminMiddleware(BaseCustomMiddleware):
    """Middleware для проверки админов"""
    
    async def pre_process(self, event, data):
        is_admin = event.from_user.id in config.admin.owner_ids
        data['is_admin'] = is_admin
```

### Использование в хэндлерах

```python
@dp.message_handler(commands=['test'])
async def test_handler(message: types.Message, data: dict):
    # Данные из middleware
    is_admin = data.get('is_admin', False)
    db_user = data.get('db_user')
    
    await message.answer(f"Admin: {is_admin}")
```

## ООП подход для хэндлеров

### Базовые классы

```python
class BaseCommandHandler(ABC):
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.register_handlers()
    
    @abstractmethod
    def get_command(self) -> str:
        pass
    
    @abstractmethod
    async def handle(self, message: types.Message):
        pass
    
    def register_handlers(self):
        self.dp.register_message_handler(
            self.handle,
            commands=[self.get_command()],
            chat_type='private'
        )
```

### Пример хэндлера

```python
class StartCommandHandler(BaseCommandHandler):
    def get_command(self) -> str:
        return "start"
    
    async def handle(self, message: types.Message):
        # Логика обработки команды
        await message.answer("Привет!")
```

## Архитектура базы данных

### Базовая модель

```python
class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
    
    def soft_delete(self):
        self.is_active = False
        self.save()
```

### Модели пользователей

```python
class User(BaseModel):
    user_id = IntegerField(unique=True, primary_key=True)
    username = CharField(null=True, max_length=32)
    first_name = CharField(max_length=64)
    
    # Модерация
    is_banned = BooleanField(default=False)
    warnings = IntegerField(default=0)
    
    def ban(self, reason: str = None):
        self.is_banned = True
        UserBan.create(user=self, reason=reason)
```

### Система миграций

```python
class MigrationManager:
    def migrate(self):
        """Применяет все ожидающие миграции"""
        pending = self.get_pending_migrations()
        for migration_name in pending:
            self.apply_migration(migration_name)
    
    def create_migration(self, name, description=""):
        """Создает новую миграцию"""
        # Создает SQL файлы миграции и отката
```

## Преимущества новой архитектуры

### 1. **Явная регистрация**
- Все хэндлеры регистрируются в одном месте
- Нет скрытых зависимостей
- Легко понять, какие хэндлеры активны

### 2. **Единая точка входа**
- main.py содержит всю логику запуска
- Четкое разделение ответственности
- Простота отладки

### 3. **ООП подход**
- Единый стиль для всех хэндлеров
- Автоматическая регистрация при создании
- Легкое наследование и расширение

### 4. **Улучшенная БД**
- Система миграций
- История модерации
- Мягкое удаление
- Оптимизация и резервное копирование
- Правильная структура подключения

### 5. **API архитектура**
- Базовые классы для API оберток
- Асинхронные контекстные менеджеры
- Обработка ошибок
- Легкое создание новых API

### 6. **Правильная загрузка**
- Loader отвечает только за базовую инициализацию
- BotManager управляет жизненным циклом
- Нет дублирования функциональности

### 7. **Модульность**
- Каждый компонент независим
- Легко добавлять новые функции
- Простота тестирования

## Примеры использования

### Создание нового хэндлера

```python
# handlers/users/message/commands/mycommand.py
from handlers.base_handler import BaseCommandHandler
from aiogram import types

class MyCommandHandler(BaseCommandHandler):
    def get_command(self) -> str:
        return "mycommand"
    
    async def handle(self, message: types.Message):
        await message.answer("Мой хэндлер!")

# main.py
from handlers.users.message.commands.mycommand import MyCommandHandler

# В register_handlers()
MyCommandHandler(self.dp),
```

### Добавление новой модели

```python
# models/new_model.py
from models.base import BaseModel
from peewee import CharField

class NewModel(BaseModel):
    name = CharField(max_length=100)
    description = CharField(null=True)
    
    class Meta:
        table_name = 'new_table'

# models/sqlite3_creator.py
from models.new_model import NewModel

# В self.models добавить NewModel
```

### Создание миграции

```python
# Создать миграцию
migration_manager.create_migration("add_new_field")

# Добавить SQL в файл миграции
ALTER TABLE users ADD COLUMN new_field TEXT;

# Применить миграции
migration_manager.migrate()
```

### Создание нового API

```python
# api/custom.py
from api.base import BaseAPIWrapper

class CustomAPIWrapper(BaseAPIWrapper):
    def __init__(self):
        super().__init__(base_url="https://api.example.com")
    
    async def make_request(self, method, endpoint, data=None):
        # Ваша логика
        pass
    
    async def get_data(self):
        return await self.get("data")

# Использование
async with CustomAPIWrapper() as api:
    data = await api.get_data()
```

## Рекомендации

### 1. **Создание новых хэндлеров**
- Всегда наследуйтесь от базовых классов
- Используйте ООП подход
- Регистрируйте в main.py

### 2. **Работа с БД**
- Используйте методы моделей
- Создавайте миграции для изменений схемы
- Применяйте мягкое удаление

### 3. **Структура кода**
- Следуйте принципу единственной ответственности
- Избегайте скрытых зависимостей
- Документируйте сложную логику

### 4. **Тестирование**
- Тестируйте каждый компонент отдельно
- Используйте моки для внешних зависимостей
- Проверяйте интеграцию компонентов

Эта архитектура обеспечивает масштабируемость, поддерживаемость и простоту разработки.
