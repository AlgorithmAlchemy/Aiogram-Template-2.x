from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardBuilder:
    """Базовый класс для создания клавиатур"""

    @staticmethod
    def create_keyboard(buttons: List[List[dict]], row_width: int = 2) -> InlineKeyboardMarkup:
        """Создает клавиатуру из списка кнопок"""
        keyboard = InlineKeyboardMarkup(row_width=row_width)

        for row in buttons:
            keyboard_row = []
            for button in row:
                keyboard_row.append(
                    InlineKeyboardButton(
                        text=button['text'],
                        callback_data=button['callback_data'],
                        url=button.get('url'),
                        web_app=button.get('web_app'),
                        login_url=button.get('login_url'),
                        switch_inline_query=button.get('switch_inline_query'),
                        switch_inline_query_current_chat=button.get('switch_inline_query_current_chat'),
                        callback_game=button.get('callback_game'),
                        pay=button.get('pay', False)
                    )
                )
            keyboard.add(*keyboard_row)

        return keyboard


class MainKeyboards:
    """Класс для основных клавиатур"""

    @staticmethod
    def get_main_keyboard() -> InlineKeyboardMarkup:
        """Главная клавиатура для пользователей"""
        buttons = [
            [
                {'text': '📋 Профиль', 'callback_data': 'profile'},
                {'text': '⚙️ Настройки', 'callback_data': 'settings'}
            ],
            [
                {'text': '❓ Помощь', 'callback_data': 'help'},
                {'text': 'ℹ️ О боте', 'callback_data': 'about'}
            ],
            [
                {'text': '🔗 Поддержка', 'callback_data': 'support'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_admin_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура для администраторов"""
        buttons = [
            [
                {'text': '📊 Статистика', 'callback_data': 'admin_stats'},
                {'text': '👥 Пользователи', 'callback_data': 'admin_users'}
            ],
            [
                {'text': '🚫 Бан пользователя', 'callback_data': 'admin_ban'},
                {'text': '✅ Разбан пользователя', 'callback_data': 'admin_unban'}
            ],
            [
                {'text': '📢 Рассылка', 'callback_data': 'admin_broadcast'},
                {'text': '⚙️ Настройки бота', 'callback_data': 'admin_settings'}
            ],
            [
                {'text': '💾 Резервная копия', 'callback_data': 'admin_backup'},
                {'text': '🔄 Восстановление', 'callback_data': 'admin_restore'}
            ],
            [
                {'text': '📝 Логи', 'callback_data': 'admin_logs'},
                {'text': '🔄 Перезапуск', 'callback_data': 'admin_restart'}
            ],
            [
                {'text': '🏠 Главное меню', 'callback_data': 'main_menu'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_settings_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура настроек"""
        buttons = [
            [
                {'text': '🔔 Уведомления', 'callback_data': 'settings_notifications'},
                {'text': '🌍 Язык', 'callback_data': 'settings_language'}
            ],
            [
                {'text': '🔒 Приватность', 'callback_data': 'settings_privacy'},
                {'text': '📱 Тема', 'callback_data': 'settings_theme'}
            ],
            [
                {'text': '⏰ Часовой пояс', 'callback_data': 'settings_timezone'},
                {'text': '🗑 Автоудаление', 'callback_data': 'settings_auto_delete'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'main_menu'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)


class AdminKeyboards:
    """Класс для админских клавиатур"""

    @staticmethod
    def get_user_management_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура управления пользователями"""
        buttons = [
            [
                {'text': '🚫 Бан', 'callback_data': 'admin_ban_user'},
                {'text': '✅ Разбан', 'callback_data': 'admin_unban_user'}
            ],
            [
                {'text': '🔇 Мут', 'callback_data': 'admin_mute_user'},
                {'text': '🔊 Размут', 'callback_data': 'admin_unmute_user'}
            ],
            [
                {'text': '⚠️ Предупреждение', 'callback_data': 'admin_warn_user'},
                {'text': '❌ Удалить', 'callback_data': 'admin_delete_user'}
            ],
            [
                {'text': 'ℹ️ Информация', 'callback_data': 'admin_user_info'},
                {'text': '📊 Статистика', 'callback_data': 'admin_user_stats'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'admin_panel'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_broadcast_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура для рассылки"""
        buttons = [
            [
                {'text': '📢 Всем пользователям', 'callback_data': 'broadcast_all'},
                {'text': '👥 Только активным', 'callback_data': 'broadcast_active'}
            ],
            [
                {'text': '🆕 Новым пользователям', 'callback_data': 'broadcast_new'},
                {'text': '👑 Администраторам', 'callback_data': 'broadcast_admins'}
            ],
            [
                {'text': '📊 Статистика рассылки', 'callback_data': 'broadcast_stats'},
                {'text': '📝 История рассылок', 'callback_data': 'broadcast_history'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'admin_panel'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_backup_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура для резервных копий"""
        buttons = [
            [
                {'text': '💾 Создать резервную копию', 'callback_data': 'backup_create'},
                {'text': '📥 Скачать резервную копию', 'callback_data': 'backup_download'}
            ],
            [
                {'text': '📤 Загрузить резервную копию', 'callback_data': 'backup_upload'},
                {'text': '🔄 Восстановить', 'callback_data': 'backup_restore'}
            ],
            [
                {'text': '📋 Список резервных копий', 'callback_data': 'backup_list'},
                {'text': '🗑 Удалить резервную копию', 'callback_data': 'backup_delete'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'admin_panel'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)


class UtilityKeyboards:
    """Класс для утилитарных клавиатур"""

    @staticmethod
    def get_confirm_keyboard(action: str, text_yes: str = "✅ Да", text_no: str = "❌ Нет") -> InlineKeyboardMarkup:
        """Клавиатура подтверждения действия"""
        buttons = [
            [
                {'text': text_yes, 'callback_data': f'confirm_{action}'},
                {'text': text_no, 'callback_data': 'cancel'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_back_keyboard(callback_data: str = "main_menu", text: str = "🔙 Назад") -> InlineKeyboardMarkup:
        """Клавиатура с кнопкой назад"""
        buttons = [
            [
                {'text': text, 'callback_data': callback_data}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_pagination_keyboard(
            current_page: int,
            total_pages: int,
            callback_prefix: str,
            show_first_last: bool = True
    ) -> InlineKeyboardMarkup:
        """Клавиатура пагинации"""
        buttons = []

        # Кнопки навигации
        nav_buttons = []

        if show_first_last and current_page > 1:
            nav_buttons.append({'text': '⏮', 'callback_data': f'{callback_prefix}_page_1'})

        if current_page > 1:
            nav_buttons.append({'text': '◀️', 'callback_data': f'{callback_prefix}_page_{current_page - 1}'})

        nav_buttons.append({'text': f'{current_page}/{total_pages}', 'callback_data': 'current_page'})

        if current_page < total_pages:
            nav_buttons.append({'text': '▶️', 'callback_data': f'{callback_prefix}_page_{current_page + 1}'})

        if show_first_last and current_page < total_pages:
            nav_buttons.append({'text': '⏭', 'callback_data': f'{callback_prefix}_page_{total_pages}'})

        buttons.append(nav_buttons)

        # Кнопка назад
        buttons.append([{'text': '🔙 Назад', 'callback_data': 'back'}])

        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_language_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура выбора языка"""
        buttons = [
            [
                {'text': '🇷🇺 Русский', 'callback_data': 'lang_ru'},
                {'text': '🇺🇸 English', 'callback_data': 'lang_en'}
            ],
            [
                {'text': '🇪🇸 Español', 'callback_data': 'lang_es'},
                {'text': '🇫🇷 Français', 'callback_data': 'lang_fr'}
            ],
            [
                {'text': '🇩🇪 Deutsch', 'callback_data': 'lang_de'},
                {'text': '🇨🇳 中文', 'callback_data': 'lang_zh'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'settings'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)

    @staticmethod
    def get_theme_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура выбора темы"""
        buttons = [
            [
                {'text': '☀️ Светлая', 'callback_data': 'theme_light'},
                {'text': '🌙 Темная', 'callback_data': 'theme_dark'}
            ],
            [
                {'text': '🌈 Авто', 'callback_data': 'theme_auto'},
                {'text': '🎨 Кастомная', 'callback_data': 'theme_custom'}
            ],
            [
                {'text': '🔙 Назад', 'callback_data': 'settings'}
            ]
        ]
        return KeyboardBuilder.create_keyboard(buttons)


# Экспорт функций для обратной совместимости
def get_main_keyboard() -> InlineKeyboardMarkup:
    return MainKeyboards.get_main_keyboard()


def get_admin_keyboard() -> InlineKeyboardMarkup:
    return MainKeyboards.get_admin_keyboard()


def get_settings_keyboard() -> InlineKeyboardMarkup:
    return MainKeyboards.get_settings_keyboard()


def get_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    return UtilityKeyboards.get_confirm_keyboard(action)


def get_back_keyboard(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
    return UtilityKeyboards.get_back_keyboard(callback_data)
