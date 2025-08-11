"""
Интеграционный модуль для подключения всех компонентов шаблона
"""
import logging
from typing import Optional

from data.config import config
from utils.hooks.event_hooks import EventHooks, setup_hooks
from utils.middleware.custom_middleware import (
    LoggingMiddleware, ThrottlingMiddleware, 
    AdminMiddleware, DatabaseMiddleware, MetricsMiddleware
)
from utils.api_wrappers.weather_api import WeatherAPIWrapper
from utils.api_wrappers.currency_api import CurrencyAPIWrapper
from utils.api_wrappers.news_api import NewsAPIWrapper

logger = logging.getLogger(__name__)


class TemplateIntegration:
    """Класс для интеграции всех компонентов шаблона"""
    
    def __init__(self, dispatcher):
        self.dp = dispatcher
        self.event_hooks = EventHooks()
        self.api_wrappers = {}
        
    def setup_middleware(self):
        """Настройка всех middleware"""
        try:
            # Базовое логирование
            self.dp.middleware.setup(LoggingMiddleware())
            
            # Throttling для защиты от спама
            if config.debug:
                logger.info("Setting up throttling middleware")
                self.dp.middleware.setup(ThrottlingMiddleware())
            
            # Проверка администраторов
            self.dp.middleware.setup(AdminMiddleware())
            
            # Работа с базой данных
            self.dp.middleware.setup(DatabaseMiddleware())
            
            # Метрики (если включены)
            if hasattr(config, 'enable_metrics') and config.enable_metrics:
                self.dp.middleware.setup(MetricsMiddleware())
                
            logger.info("All middleware setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up middleware: {e}")
    
    def setup_api_wrappers(self):
        """Настройка API wrappers"""
        try:
            # Weather API
            if hasattr(config, 'weather_api_key') and config.weather_api_key:
                self.api_wrappers['weather'] = WeatherAPIWrapper(
                    api_key=config.weather_api_key
                )
            
            # Currency API
            if hasattr(config, 'currency_api_key') and config.currency_api_key:
                self.api_wrappers['currency'] = CurrencyAPIWrapper(
                    api_key=config.currency_api_key
                )
            
            # News API
            if hasattr(config, 'news_api_key') and config.news_api_key:
                self.api_wrappers['news'] = NewsAPIWrapper(
                    api_key=config.news_api_key
                )
                
            logger.info(f"API wrappers setup completed: {list(self.api_wrappers.keys())}")
            
        except Exception as e:
            logger.error(f"Error setting up API wrappers: {e}")
    
    def setup_event_hooks(self):
        """Настройка event hooks"""
        try:
            setup_hooks(self.event_hooks)
            logger.info("Event hooks setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up event hooks: {e}")
    
    def setup_fsm_states(self):
        """Настройка FSM состояний"""
        try:
            # Импортируем состояния
            from states.user.registration import RegistrationStates
            from states.admin.broadcast import BroadcastStates
            
            # Регистрируем состояния в диспетчере
            self.dp.storage.register_states([
                RegistrationStates,
                BroadcastStates
            ])
            
            logger.info("FSM states setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up FSM states: {e}")
    
    def get_api_wrapper(self, name: str) -> Optional[object]:
        """Получить API wrapper по имени"""
        return self.api_wrappers.get(name)
    
    def execute_startup_hooks(self):
        """Выполнить startup hooks"""
        try:
            self.event_hooks.execute_startup_hooks()
            logger.info("Startup hooks executed")
            
        except Exception as e:
            logger.error(f"Error executing startup hooks: {e}")
    
    def execute_shutdown_hooks(self):
        """Выполнить shutdown hooks"""
        try:
            self.event_hooks.execute_shutdown_hooks()
            logger.info("Shutdown hooks executed")
            
        except Exception as e:
            logger.error(f"Error executing shutdown hooks: {e}")
    
    def setup_all(self):
        """Настройка всех компонентов"""
        logger.info("Starting template integration setup...")
        
        self.setup_middleware()
        self.setup_api_wrappers()
        self.setup_event_hooks()
        self.setup_fsm_states()
        
        logger.info("Template integration setup completed")


def create_integration(dispatcher) -> TemplateIntegration:
    """Создать экземпляр интеграции"""
    return TemplateIntegration(dispatcher)
