"""
Базовый класс для API оберток
"""
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
