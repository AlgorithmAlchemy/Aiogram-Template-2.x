import logging
from typing import Dict, Any
from api.base import BaseAPIWrapper
from data.config import config

logger = logging.getLogger(__name__)


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
    
    async def get_forecast(self, city: str) -> Dict[str, Any]:
        """Получить прогноз погоды для города"""
        return await self.get('forecast', {'q': city, 'units': 'metric'})
