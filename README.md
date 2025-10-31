# Aiogram 2.x Template - Современная Архитектура

Современный шаблон для Telegram ботов на aiogram 2.x с правильной архитектурой, ООП подходом и лучшими практиками.

## Особенности

- ** Правильная архитектура** - четкое разделение ответственности
- ** ООП подход** - все хэндлеры наследуются от базовых классов
- ** Улучшенная БД** - система миграций, история модерации, мягкое удаление
- ** Middleware** - в правильном месте, с базовыми классами
- ** API архитектура** - асинхронные обертки для внешних API
- ** Явная регистрация** - все компоненты регистрируются в main.py
- ** Масштабируемость** - легко добавлять новые функции
- ** Тестируемость** - каждый компонент независим

## Структура проекта

```
├── main.py                     # Главная точка входа
├── loader.py                   # ️ Базовая инициализация
├── data/                       #  Конфигурация
├── models/                     # ️ Модели БД
│   ├── base.py                 # Базовая модель
│   ├── user.py                 # Модели пользователей
│   └── sqlite3_creator.py      # Менеджер БД
├── database/                   # Подключение к БД
│   └── connection.py           # Настройки подключения
├── api/                        # Внешние API
│   ├── base.py                 # Базовый класс API
│   ├── weather.py              # API погоды
│   └── currency.py             # API валют
├── handlers/                   # Обработчики
│   ├── base_handler.py         # Базовые классы
│   └── users/message/commands/ # Команды
├── middleware/                 # Middleware
│   ├── base.py                 # Базовый класс
│   ├── logging.py              # Логирование
│   ├── throttling.py           # Ограничение частоты
│   ├── admin.py                # Проверка админов
│   └── database.py             # Работа с БД
├── utils/                      # Утилиты
├── filters/                    # Фильтры
├── states/                     # FSM состояния
├── keyboards/                  # Клавиатуры
├── examples/                   # Примеры
└── docs/                       # Документация
```

## Быстрый старт

### 1. Установка

```bash
git clone https://github.com/your-username/aiogram-template.git
cd aiogram-template
pip install -r requirements.txt
```

### 2. Настройка

```bash
cp data/config.example.py data/config.py
# Отредактируйте config.py с вашими настройками
```

### 3. Запуск

```bash
python bot.py
```

## Архитектура

### Loader (loader.py)

Базовый загрузчик для инициализации бота:

- Настройка хранилища (Memory/Redis)
- Создание экземпляра бота
- Создание диспетчера

### BotManager (main.py)

Центральный класс для управления жизненным циклом:

- Подключение к БД
- Регистрация хэндлеров
- Настройка middleware
- Управление запуском/остановкой

### ООП Хэндлеры

Все хэндлеры наследуются от базовых классов:

```python
class StartCommandHandler(BaseCommandHandler):
    def get_command(self) -> str:
        return "start"

    async def handle(self, message: types.Message):
        await message.answer("Привет!")
```

### Middleware

Правильная структура middleware с базовыми классами:

```python
class LoggingMiddleware(BaseCustomMiddleware):
    async def pre_process(self, event, data):
        logger.info(f"Message from {event.from_user.id}")
```

### API Архитектура

Асинхронные обертки для внешних API:

```python
async with WeatherAPIWrapper() as api:
    weather = await api.get_weather("Moscow")
```

## 📚 Примеры

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


# bot.py
from handlers.users.message.commands.mycommand import MyCommandHandler

MyCommandHandler(self.dp),
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


# Использование
async with CustomAPIWrapper() as api:
    data = await api.get("endpoint")
```

### Создание новой модели

```python
# models/new_model.py
from models.base import BaseModel
from peewee import CharField

class NewModel(BaseModel):
    name = CharField(max_length=100)
    description = CharField(null=True)
    
    class Meta:
        table_name = 'new_table'
```

## Конфигурация

### Основные настройки

```python
# data/config.py
BOT_TOKEN = "your_bot_token"
ADMIN_IDS = [123456789]
DEBUG = True

# Redis (опционально)
USE_REDIS = False
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

### API ключи

```python
# API ключи для внешних сервисов
WEATHER_API_KEY = "your_openweathermap_key"
CURRENCY_API_KEY = "your_exchangerate_key"
```

## 🛠️ Разработка

### Добавление новых функций

1. **Хэндлеры** - наследуйтесь от базовых классов
2. **API** - используйте BaseAPIWrapper
3. **Middleware** - наследуйтесь от BaseCustomMiddleware
4. **Модели** - наследуйтесь от BaseModel
5. **Регистрация** - добавьте в main.py

### Тестирование

```bash
# Запуск примеров
python examples/oop_handlers_example.py
python examples/api_examples.py
python examples/middleware_examples.py
```

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## Благодарности

- [aiogram](https://github.com/aiogram/aiogram) - отличная библиотека для Telegram ботов
- [Peewee](https://github.com/coleifer/peewee) - легкий ORM
- Сообщество разработчиков Telegram ботов

## 📞 Поддержкаe

- 🐛 Issues: [GitHub Issues](https://github.com/your-username/aiogram-template/issues)

---

⭐ Если этот проект вам помог, поставьте звездочку!
