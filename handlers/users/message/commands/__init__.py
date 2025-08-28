# Импорт всех команд для автоматической регистрации
from . import about
from . import ban_user
from . import commands
from . import echo
from . import feedback
from . import help
from . import menu
from . import ping
from . import profile
from . import register
from . import settings
from . import start
from . import stats
from . import status
from . import support
from . import unban_user
from . import uptime
from . import users
from . import version
from . import warn_user
from . import weather

__all__ = [
    'start',
    'menu',
    'about',
    'version',
    'status',
    'ping',
    'uptime',
    'help',
    'commands',
    'profile',
    'settings',
    'feedback',
    'support',
    'echo',
    'ban_user',
    'unban_user',
    'warn_user',
    'stats',
    'users',
    'register',
    'weather'
]
