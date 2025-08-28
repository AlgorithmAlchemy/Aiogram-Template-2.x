import asyncio
import logging

from api.currency import CurrencyAPIWrapper
from api.weather import WeatherAPIWrapper

logger = logging.getLogger(__name__)


async def weather_api_example():
    """Пример использования API погоды"""
    print("=== Weather API Example ===")

    async with WeatherAPIWrapper() as weather_api:
        # Получаем текущую погоду
        weather = await weather_api.get_weather("Moscow")
        print(f"Weather in Moscow: {weather}")

        # Получаем прогноз
        forecast = await weather_api.get_forecast("Moscow")
        print(f"Forecast in Moscow: {forecast}")

    print("=== Weather API Example Completed ===")


async def currency_api_example():
    """Пример использования API валют"""
    print("=== Currency API Example ===")

    async with CurrencyAPIWrapper() as currency_api:
        # Получаем курс обмена
        rate = await currency_api.get_exchange_rate("USD", "RUB")
        print(f"USD to RUB rate: {rate}")

        # Получаем список валют
        currencies = await currency_api.get_currencies()
        print(f"Available currencies: {currencies}")

    print("=== Currency API Example Completed ===")


async def custom_api_example():
    """Пример создания кастомного API"""
    print("=== Custom API Example ===")

    from api.base import BaseAPIWrapper

    class CustomAPIWrapper(BaseAPIWrapper):
        """Кастомный API wrapper"""

        def __init__(self):
            super().__init__(
                base_url="https://jsonplaceholder.typicode.com"
            )

        async def make_request(self, method: str, endpoint: str,
                               data: dict = None) -> dict:
            """Выполнить запрос"""
            try:
                url = f"{self.base_url}/{endpoint}"

                async with self.session.request(method, url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {'error': f'HTTP {response.status}'}
            except Exception as e:
                return self.handle_error(e)

        async def get_posts(self):
            """Получить посты"""
            return await self.get("posts")

        async def get_post(self, post_id: int):
            """Получить пост по ID"""
            return await self.get(f"posts/{post_id}")

    # Используем кастомный API
    async with CustomAPIWrapper() as api:
        posts = await api.get_posts()
        print(f"Posts: {len(posts)} items")

        post = await api.get_post(1)
        print(f"Post 1: {post.get('title', 'No title')}")

    print("=== Custom API Example Completed ===")


async def error_handling_example():
    """Пример обработки ошибок API"""
    print("=== Error Handling Example ===")

    from api.base import BaseAPIWrapper

    class ErrorAPIWrapper(BaseAPIWrapper):
        """API wrapper для демонстрации ошибок"""

        def __init__(self):
            super().__init__(base_url="https://invalid-url.com")

        async def make_request(self, method: str, endpoint: str,
                               data: dict = None) -> dict:
            """Выполнить запрос (всегда вызывает ошибку)"""
            try:
                url = f"{self.base_url}/{endpoint}"
                async with self.session.request(method, url) as response:
                    return await response.json()
            except Exception as e:
                return self.handle_error(e)

    # Тестируем обработку ошибок
    async with ErrorAPIWrapper() as api:
        result = await api.get("test")
        print(f"Error result: {result}")

    print("=== Error Handling Example Completed ===")


async def main():
    """Главная функция для демонстрации"""
    print("=== API Examples ===")

    # Примеры API
    await weather_api_example()
    await currency_api_example()
    await custom_api_example()
    await error_handling_example()

    print("\n=== All API Examples Completed ===")


if __name__ == "__main__":
    asyncio.run(main())
