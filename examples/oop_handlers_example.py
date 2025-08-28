import logging

from aiogram import types
from aiogram.types import ParseMode

from handlers.base_handler import BaseCommandHandler, BaseMessageHandler, BaseCallbackHandler
from loader import dp

logger = logging.getLogger(__name__)


class ExampleCommandHandler(BaseCommandHandler):
    """Пример обработчика команды"""

    def get_command(self) -> str:
        return "example"

    async def handle(self, message: types.Message):
        """Обработчик команды /example"""
        await message.answer(
            "Это пример обработчика команды в ООП стиле!",
            parse_mode=ParseMode.HTML
        )


class ExampleMessageHandler(BaseMessageHandler):
    """Пример обработчика сообщений"""

    def get_content_types(self) -> list:
        return ['photo', 'document']

    async def handle(self, message: types.Message):
        """Обработчик фото и документов"""
        if message.photo:
            await message.answer("Получено фото!")
        elif message.document:
            await message.answer("Получен документ!")


class ExampleCallbackHandler(BaseCallbackHandler):
    """Пример обработчика callback запросов"""

    def get_callback_data(self) -> str:
        return "example_button"

    async def handle(self, callback_query: types.CallbackQuery):
        """Обработчик callback"""
        await callback_query.answer("Кнопка нажата!")
        await callback_query.message.answer("Обработка callback в ООП стиле!")


class AdvancedCommandHandler(BaseCommandHandler):
    """Продвинутый пример обработчика команды"""

    def __init__(self, dp):
        super().__init__(dp)
        self.counter = 0

    def get_command(self) -> str:
        return "counter"

    async def handle(self, message: types.Message):
        """Обработчик с внутренним состоянием"""
        self.counter += 1
        await message.answer(
            f"Счетчик: {self.counter}",
            parse_mode=ParseMode.HTML
        )


class AdminCommandHandler(BaseCommandHandler):
    """Пример админского обработчика"""

    def get_command(self) -> str:
        return "admin"

    async def handle(self, message: types.Message):
        """Обработчик только для админов"""
        # Проверка на админа
        if message.from_user.id not in [123456789]:  # ID админов
            await message.answer("❌ У вас нет прав администратора!")
            return

        await message.answer(
            "👑 Добро пожаловать в админскую панель!",
            parse_mode=ParseMode.HTML
        )


class MultiCommandHandler(BaseCommandHandler):
    """Пример обработчика с несколькими командами"""

    def __init__(self, dp, command: str):
        self._command = command
        super().__init__(dp)

    def get_command(self) -> str:
        return self._command

    async def handle(self, message: types.Message):
        """Обработчик для разных команд"""
        command = message.get_command()
        await message.answer(f"Обработана команда: {command}")


def create_handlers():
    """Создание всех хэндлеров"""

    # Создаем экземпляры хэндлеров
    example_cmd = ExampleCommandHandler(dp)
    example_msg = ExampleMessageHandler(dp)
    example_callback = ExampleCallbackHandler(dp)
    advanced_cmd = AdvancedCommandHandler(dp)
    admin_cmd = AdminCommandHandler(dp)

    # Создаем несколько хэндлеров с разными командами
    cmd1 = MultiCommandHandler(dp, "cmd1")
    cmd2 = MultiCommandHandler(dp, "cmd2")
    cmd3 = MultiCommandHandler(dp, "cmd3")

    logger.info("All example handlers created successfully!")

    return [
        example_cmd,
        example_msg,
        example_callback,
        advanced_cmd,
        admin_cmd,
        cmd1,
        cmd2,
        cmd3
    ]


def main():
    """Демонстрация ООП подхода"""
    print("=== Демонстрация ООП подхода для хэндлеров ===")

    # Создаем хэндлеры
    handlers = create_handlers()

    print(f"Создано {len(handlers)} хэндлеров")
    print("Все хэндлеры автоматически зарегистрированы!")

    print("\nПреимущества ООП подхода:")
    print("✅ Единый стиль для всех хэндлеров")
    print("✅ Автоматическая регистрация")
    print("✅ Возможность добавления состояния")
    print("✅ Легкое наследование и расширение")
    print("✅ Чистый и понятный код")

    print("\n=== Демонстрация завершена ===")


if __name__ == "__main__":
    main()
