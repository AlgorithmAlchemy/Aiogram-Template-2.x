import logging
from datetime import datetime
from typing import List, Dict, Optional, Any, Union, TypeVar, Callable, Awaitable

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from peewee import Model

# Типы для моделей
T = TypeVar('T', bound=Model)

# Типы для хэндлеров
HandlerFunc = Callable[[types.Message], Awaitable[None]]
CallbackFunc = Callable[[types.CallbackQuery], Awaitable[None]]

logger = logging.getLogger(__name__)


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ ХЭНДЛЕРОВ
# ============================================================================

class TypedCommandHandler:
    """Пример хэндлера с правильной типизацией"""

    def __init__(self, dp: Dispatcher) -> None:
        self.dp: Dispatcher = dp
        self.command: str = "example"
        self.register_handler()

    def register_handler(self) -> None:
        """Регистрация хэндлера с типизацией"""
        self.dp.register_message_handler(
            self.handle,
            commands=[self.command],
            chat_type='private'
        )

    async def handle(self, message: types.Message) -> None:
        """Обработчик с типизацией"""
        user_id: int = message.from_user.id
        username: Optional[str] = message.from_user.username
        text: str = message.text or ""

        logger.info(f"Message from {user_id}: {text}")
        await message.answer(f"Hello, {username or 'User'}!")


class TypedCallbackHandler:
    """Пример callback хэндлера с типизацией"""

    def __init__(self, dp: Dispatcher) -> None:
        self.dp: Dispatcher = dp
        self.callback_data: str = "example_callback"
        self.register_handler()

    def register_handler(self) -> None:
        """Регистрация callback хэндлера"""
        self.dp.register_callback_query_handler(
            self.handle,
            lambda c: c.data == self.callback_data
        )

    async def handle(self, callback_query: types.CallbackQuery) -> None:
        """Обработчик callback с типизацией"""
        user_id: int = callback_query.from_user.id
        data: str = callback_query.data or ""

        logger.info(f"Callback from {user_id}: {data}")
        await callback_query.answer("Callback processed!")


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ МОДЕЛЕЙ
# ============================================================================

class TypedUserModel:
    """Пример модели с типизацией"""

    def __init__(self, user_id: int, username: str) -> None:
        self.user_id: int = user_id
        self.username: str = username
        self.created_at: datetime = datetime.now()
        self.is_active: bool = True

    @classmethod
    def get_by_id(cls: type, user_id: int) -> Optional['TypedUserModel']:
        """Получение пользователя по ID с типизацией"""
        try:
            # Здесь была бы логика получения из БД
            return cls(user_id, "example_user")
        except Exception:
            return None

    @classmethod
    def get_active_users(cls: type) -> List['TypedUserModel']:
        """Получение активных пользователей с типизацией"""
        # Здесь была бы логика получения из БД
        return [cls(1, "user1"), cls(2, "user2")]

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь с типизацией"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ MIDDLEWARE
# ============================================================================

class TypedMiddleware:
    """Пример middleware с типизацией"""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.processed_count: int = 0

    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[types.Message, types.CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        """Вызов middleware с типизацией"""
        self.processed_count += 1

        # Предобработка
        await self.pre_process(event, data)

        # Выполнение обработчика
        result: Any = await handler(event, data)

        # Постобработка
        await self.post_process(event, data, result)

        return result

    async def pre_process(
            self,
            event: Union[types.Message, types.CallbackQuery],
            data: Dict[str, Any]
    ) -> None:
        """Предобработка с типизацией"""
        user_id: int = event.from_user.id
        logger.info(f"Pre-processing for user {user_id}")

    async def post_process(
            self,
            event: Union[types.Message, types.CallbackQuery],
            data: Dict[str, Any],
            result: Any
    ) -> None:
        """Постобработка с типизацией"""
        user_id: int = event.from_user.id
        logger.info(f"Post-processing for user {user_id}")


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ API
# ============================================================================

class TypedAPIWrapper:
    """Пример API обертки с типизацией"""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.timeout: int = 30

    async def make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Выполнение запроса с типизацией"""
        url: str = f"{self.base_url}/{endpoint}"
        headers: Dict[str, str] = {"Authorization": f"Bearer {self.api_key}"}

        # Здесь была бы логика выполнения запроса
        return {
            'success': True,
            'data': data or {},
            'url': url
        }

    async def get_data(self, endpoint: str) -> Dict[str, Any]:
        """GET запрос с типизацией"""
        return await self.make_request('GET', endpoint)

    async def post_data(
            self,
            endpoint: str,
            data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """POST запрос с типизацией"""
        return await self.make_request('POST', endpoint, data)


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ FSM
# ============================================================================

class TypedFSMHandler:
    """Пример FSM хэндлера с типизацией"""

    async def start_conversation(self, message: types.Message) -> None:
        """Начало диалога с типизацией"""
        user_id: int = message.from_user.id
        await message.answer("Введите ваше имя:")
        # Здесь был бы переход в состояние

    async def process_name(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """Обработка имени с типизацией"""
        name: str = message.text or ""
        user_id: int = message.from_user.id

        # Сохранение данных в состоянии
        await state.update_data(name=name, user_id=user_id)

        await message.answer(f"Привет, {name}! Введите ваш возраст:")
        # Здесь был бы переход в следующее состояние

    async def process_age(
            self,
            message: types.Message,
            state: FSMContext
    ) -> None:
        """Обработка возраста с типизацией"""
        try:
            age: int = int(message.text or "0")
            data: Dict[str, Any] = await state.get_data()
            name: str = data.get('name', 'Unknown')

            await message.answer(f"{name}, ваш возраст: {age}")
            await state.finish()

        except ValueError:
            await message.answer("Пожалуйста, введите корректный возраст")


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ УТИЛИТ
# ============================================================================

class TypedUtils:
    """Пример утилит с типизацией"""

    @staticmethod
    def format_user_info(user: types.User) -> Dict[str, Any]:
        """Форматирование информации о пользователе с типизацией"""
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_bot': user.is_bot,
            'language_code': user.language_code
        }

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Валидация телефона с типизацией"""
        import re
        pattern: str = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def parse_command_args(text: str) -> List[str]:
        """Парсинг аргументов команды с типизацией"""
        parts: List[str] = text.split()
        return parts[1:] if len(parts) > 1 else []


# ============================================================================
# ПРИМЕРЫ ТИПИЗАЦИИ ДЛЯ КОНФИГУРАЦИИ
# ============================================================================

class TypedConfig:
    """Пример конфигурации с типизацией"""

    def __init__(self) -> None:
        self.bot_token: str = "your_bot_token"
        self.admin_ids: List[int] = [123456789]
        self.debug: bool = True
        self.database_url: str = "sqlite:///bot.db"
        self.redis_url: Optional[str] = None

    def get_admin_ids(self) -> List[int]:
        """Получение ID администраторов с типизацией"""
        return self.admin_ids.copy()

    def is_admin(self, user_id: int) -> bool:
        """Проверка администратора с типизацией"""
        return user_id in self.admin_ids

    def get_database_config(self) -> Dict[str, Any]:
        """Получение конфигурации БД с типизацией"""
        return {
            'url': self.database_url,
            'echo': self.debug
        }


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

async def example_usage() -> None:
    """Пример использования типизированных компонентов"""

    # Создание экземпляров
    config: TypedConfig = TypedConfig()
    utils: TypedUtils = TypedUtils()

    # Работа с пользователями
    user_model: TypedUserModel = TypedUserModel(1, "test_user")
    user_dict: Dict[str, Any] = user_model.to_dict()

    # Работа с API
    api: TypedAPIWrapper = TypedAPIWrapper("https://api.example.com", "key")
    result: Dict[str, Any] = await api.get_data("users")

    # Работа с middleware
    middleware: TypedMiddleware = TypedMiddleware("example")

    logger.info("All typed components created successfully")


if __name__ == "__main__":
    # Демонстрация типизации
    import asyncio


    async def main() -> None:
        await example_usage()
        print("✅ Все примеры типизации выполнены успешно!")


    asyncio.run(main())
