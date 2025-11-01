import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)


class BaseAPIWrapper(ABC):
    def __init__(self, base_url: str, timeout: int = 30) -> None:
        self.base_url: str = base_url.rstrip('/')
        self.timeout: int = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> 'BaseAPIWrapper':
        """Asynchronous Context Manager - Login"""
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
        """Asynchronous Context Manager - Exit"""
        if self.session:
            await self.session.close()

    @abstractmethod
    async def make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Abstract method for executing queries"""
        pass

    async def get(self, endpoint: str) -> Dict[str, Any]:
        """GET queri"""
        return await self.make_request('GET', endpoint)

    async def post(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """POST queri"""
        return await self.make_request('POST', endpoint, data)

    async def put(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """PUT queri"""
        return await self.make_request('PUT', endpoint, data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE queri"""
        return await self.make_request('DELETE', endpoint)

    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """API error handling"""
        logger.error(f"API Error: {error}")
        return {
            'success': False,
            'error': str(error),
            'data': None
        }

    def build_url(self, endpoint: str) -> str:
        """Building a full URL"""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
