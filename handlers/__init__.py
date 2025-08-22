"""
Автоматическая регистрация всех хэндлеров
"""
from loader import dp

# Импортируем все хэндлеры для автоматической регистрации
from handlers.users.message.commands.start import start_handler
from handlers.users.message.commands.profile import profile_handler
from handlers.users.message.commands.ban_user import ban_user_handler
from handlers.users.message.commands.unban_user import unban_user_handler
from handlers.users.message.commands.warn_user import warn_user_handler
from handlers.users.message.commands.echo import echo_handler

# Импортируем остальные хэндлеры команд
from handlers.users.message.commands.help import HelpCommandHandler
from handlers.users.message.commands.about import AboutCommandHandler
from handlers.users.message.commands.settings import SettingsCommandHandler
from handlers.users.message.commands.stats import StatsCommandHandler
from handlers.users.message.commands.users import UsersCommandHandler
from handlers.users.message.commands.status import StatusCommandHandler
from handlers.users.message.commands.version import VersionCommandHandler
from handlers.users.message.commands.uptime import UptimeCommandHandler
from handlers.users.message.commands.commands import CommandsCommandHandler
from handlers.users.message.commands.menu import MenuCommandHandler
from handlers.users.message.commands.ping import PingCommandHandler
from handlers.users.message.commands.feedback import FeedbackCommandHandler
from handlers.users.message.commands.support import SupportCommandHandler
from handlers.users.message.commands.weather import WeatherCommandHandler

# Создаем экземпляры всех хэндлеров для автоматической регистрации
help_handler = HelpCommandHandler(dp)
about_handler = AboutCommandHandler(dp)
settings_handler = SettingsCommandHandler(dp)
stats_handler = StatsCommandHandler(dp)
users_handler = UsersCommandHandler(dp)
status_handler = StatusCommandHandler(dp)
version_handler = VersionCommandHandler(dp)
uptime_handler = UptimeCommandHandler(dp)
commands_handler = CommandsCommandHandler(dp)
menu_handler = MenuCommandHandler(dp)
ping_handler = PingCommandHandler(dp)
feedback_handler = FeedbackCommandHandler(dp)
support_handler = SupportCommandHandler(dp)
weather_handler = WeatherCommandHandler(dp)

logger = logging.getLogger(__name__)
logger.info("All handlers registered successfully!")
