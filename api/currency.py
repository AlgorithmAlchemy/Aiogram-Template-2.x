import logging
from typing import Dict, Any

from api.base import BaseAPIWrapper
from data.config import config

logger = logging.getLogger(__name__)


class CurrencyAPIWrapper(BaseAPIWrapper):
    def __init__(self, api_key: str = None):
        super().__init__(
            api_key=api_key or config.api.currency_api_key,
            base_url="https://api.exchangerate-api.com/v4"
        )

    async def make_request(self, method: str, endpoint: str,
                           data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the Currencies API"""
        try:
            url = f"{self.base_url}/{endpoint}"
            params = data or {}

            async with self.session.request(method, url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': f'HTTP {response.status}'}
        except Exception as e:
            return self.handle_error(e)

    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        return await self.get(f"latest/{from_currency.upper()}")

    async def get_currencies(self) -> Dict[str, Any]:
        return await self.get("latest/USD")
