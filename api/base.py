import aiohttp
import logging
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseAPIWrapper(ABC):
    """Базовый класс для всех API оберток"""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        self.base_url: str = base_url.rstrip('/')
        self.timeout: int = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> 'BaseAPIWrapper':
        """Асинхронный контекстный менеджер - вход"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self

    async def __aexit__(
        self, 
        exc_type: Any, 
        exc_val: Any, 
        exc_tb: Any
    ) -> None:
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()

    @abstractmethod
    async def make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Абстрактный метод для выполнения запросов"""
        pass

    async def get(self, endpoint: str) -> Dict[str, Any]:
        """GET запрос"""
        return await self.make_request('GET', endpoint)

    async def post(
        self, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """POST запрос"""
        return await self.make_request('POST', endpoint, data)

    async def put(
        self, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """PUT запрос"""
        return await self.make_request('PUT', endpoint, data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE запрос"""
        return await self.make_request('DELETE', endpoint)

    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Обработка ошибок API"""
        logger.error(f"API Error: {error}")
        return {
            'success': False,
            'error': str(error),
            'data': None
        }

    def build_url(self, endpoint: str) -> str:
        """Построение полного URL"""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
