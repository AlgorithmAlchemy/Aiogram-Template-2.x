from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура для пользователей"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("📋 Профиль", callback_data="profile"),
        InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
    )
    keyboard.add(
        InlineKeyboardButton("❓ Помощь", callback_data="help"),
        InlineKeyboardButton("ℹ️ О боте", callback_data="about")
    )
    keyboard.add(
        InlineKeyboardButton("🔗 Поддержка", callback_data="support")
    )
    
    return keyboard


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для администраторов"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")
    )
    keyboard.add(
        InlineKeyboardButton("🚫 Бан пользователя", callback_data="admin_ban"),
        InlineKeyboardButton("✅ Разбан пользователя", callback_data="admin_unban")
    )
    keyboard.add(
        InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast"),
        InlineKeyboardButton("⚙️ Настройки бота", callback_data="admin_settings")
    )
    keyboard.add(
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    return keyboard


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура настроек"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("🔔 Уведомления", callback_data="settings_notifications"),
        InlineKeyboardButton("🌍 Язык", callback_data="settings_language")
    )
    keyboard.add(
        InlineKeyboardButton("🔒 Приватность", callback_data="settings_privacy"),
        InlineKeyboardButton("📱 Тема", callback_data="settings_theme")
    )
    keyboard.add(
        InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
    )
    
    return keyboard


def get_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения действия"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton("✅ Да", callback_data=f"confirm_{action}"),
        InlineKeyboardButton("❌ Нет", callback_data="cancel")
    )
    
    return keyboard


def get_back_keyboard(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой назад"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=callback_data))
    
    return keyboard
