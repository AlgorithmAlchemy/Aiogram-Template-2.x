import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from data.config import config

logger = logging.getLogger(__name__)


class BaseAPIWrapper(ABC):
    """Базовый класс для API оберток"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def make_request(self, method: str, endpoint: str, 
                          data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполнить запрос к API"""
        pass
    
    async def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """GET запрос"""
        return await self.make_request('GET', endpoint, params)
    
    async def post(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """POST запрос"""
        return await self.make_request('POST', endpoint, data)
    
    async def put(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """PUT запрос"""
        return await self.make_request('PUT', endpoint, data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE запрос"""
        return await self.make_request('DELETE', endpoint)
    
    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Обработка ошибок API"""
        logger.error(f"API Error: {error}")
        return {
            'success': False,
            'error': str(error),
            'data': None
        }


class WeatherAPIWrapper(BaseAPIWrapper):
    """Обертка для API погоды"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            api_key=api_key or config.api.weather_api_key,
            base_url="https://api.openweathermap.org/data/2.5"
        )
    
    async def make_request(self, method: str, endpoint: str, 
                          data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполнить запрос к API погоды"""
        try:
            url = f"{self.base_url}/{endpoint}"
            params = data or {}
            params['appid'] = self.api_key
            
            async with self.session.request(method, url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': f'HTTP {response.status}'}
        except Exception as e:
            return self.handle_error(e)
    
    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Получить погоду для города"""
        return await self.get('weather', {'q': city, 'units': 'metric'})


class CurrencyAPIWrapper(BaseAPIWrapper):
    """Обертка для API валют"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            api_key=api_key or config.api.currency_api_key,
            base_url="https://api.exchangerate-api.com/v4"
        )
    
    async def make_request(self, method: str, endpoint: str, 
                          data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполнить запрос к API валют"""
        try:
            url = f"{self.base_url}/{endpoint}"
            
            async with self.session.request(method, url, params=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': f'HTTP {response.status}'}
        except Exception as e:
            return self.handle_error(e)
    
    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Получить курс обмена валют"""
        return await self.get(f'latest/{from_currency.upper()}')


class NewsAPIWrapper(BaseAPIWrapper):
    """Обертка для API новостей"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            api_key=api_key or config.api.news_api_key,
            base_url="https://newsapi.org/v2"
        )
    
    async def make_request(self, method: str, endpoint: str, 
                          data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполнить запрос к API новостей"""
        try:
            url = f"{self.base_url}/{endpoint}"
            params = data or {}
            params['apiKey'] = self.api_key
            
            async with self.session.request(method, url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': f'HTTP {response.status}'}
        except Exception as e:
            return self.handle_error(e)
    
    async def get_top_headlines(self, country: str = 'ru', category: str = None) -> Dict[str, Any]:
        """Получить топ новости"""
        params = {'country': country}
        if category:
            params['category'] = category
        return await self.get('top-headlines', params)
