from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def terms_of_use_menu():
    terms_of_use_accept = InlineKeyboardButton('Хочу подключить 👌', callback_data='accept_terms_of_use')
    menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu.add(terms_of_use_accept)
    return menu


def home_menu(demo_or_full, link=None):
    print(11111111111, demo_or_full)
    demo_or_full = str(demo_or_full).strip()
    print(demo_or_full, type(demo_or_full))
    if demo_or_full == 'pre_demo':
        fast_connect = InlineKeyboardButton('Получить пробный период 🎁️', callback_data='get_free_time')
        instructions = InlineKeyboardButton("Инструкция 🧐", url="http://localvpnbot.ru/manual")
        subscribe = InlineKeyboardButton('Полный доступ ⚡️', callback_data='subscribe')
        support = InlineKeyboardButton('Поддержка ✌️', callback_data='support')
        menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu.add(fast_connect, instructions, subscribe, support)

    elif demo_or_full == 'demo_activate':
        fast_connect = InlineKeyboardButton('Подключить VPN ✅', url=link)
        instructions = InlineKeyboardButton("Инструкция 🧐", url="http://localvpnbot.ru/manual")
        subscribe = InlineKeyboardButton('Полный доступ ⚡️', callback_data='subscribe')
        support = InlineKeyboardButton('Поддержка ✌️', callback_data='support')
        menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu.add(fast_connect, instructions, subscribe, support)

    elif demo_or_full == 'full':
        fast_connect = InlineKeyboardButton('Подключить VPN ✅', url=link)
        instructions = InlineKeyboardButton("Инструкция 🧐", url="http://localvpnbot.ru/manual")
        support = InlineKeyboardButton('Поддержка ✌️', callback_data='support')
        menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu.add(fast_connect, instructions, support)

    elif demo_or_full == 'ended':
        instructions = InlineKeyboardButton("Инструкция 🧐", url="http://localvpnbot.ru/manual")
        subscribe = InlineKeyboardButton('Продлить подписку ⚡️', callback_data='subscribe')
        support = InlineKeyboardButton('Поддержка ✌️', callback_data='support')
        menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu.add(subscribe, instructions, support)
    return menu


def main_menu_limited_access():
    subscribe_extend = InlineKeyboardButton('💳 Продлить подписку', callback_data='subscribe')
    support = InlineKeyboardButton('🙋🏻‍♂️Поддержка', callback_data='support')
    menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu.add(subscribe_extend, support)
    return menu


def prolong_24_sub():
    subscribe = InlineKeyboardButton('Продлить подписку ⚡️', callback_data='subscribe')
    menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu.add(subscribe)
    return


def region_selection_menu(demo_or_full, access_days=None):
    keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    instructions = InlineKeyboardButton("📖Инструкция", callback_data="instructions")
    back = InlineKeyboardButton("<Назад", callback_data="back_region_menu")

    if demo_or_full == 'demo':
        netherlands_button = InlineKeyboardButton("🇳🇱 Нидерланды", callback_data="netherlands")
        keyboard.add(netherlands_button, instructions, back)
    else:
        # finland_button = InlineKeyboardButton("🇫🇮 Финляндия", callback_data="finland")
        # kazakhstan_button = InlineKeyboardButton("🇰🇿 Казахстан", callback_data="kazakhstan")
        # germany_button = InlineKeyboardButton("🇩🇪 Германия", callback_data="germany")
        # austria_button = InlineKeyboardButton("🇦🇹 Австрия", callback_data="austria")
        russia_button = InlineKeyboardButton("🇷🇺 Россия", callback_data="russia")
        # india_button = InlineKeyboardButton("🇮🇳 Индия", callback_data="india")
        netherlands_button = InlineKeyboardButton("🇳🇱 Нидерланды", callback_data="netherlands")
        usa_button = InlineKeyboardButton("🇺🇸 США", callback_data="usa")
        keyboard.add(russia_button, netherlands_button, usa_button, instructions, back)

    return keyboard


def support_menu():
    not_work_outline = InlineKeyboardButton('Не работает Outline', callback_data='not_work_outline')
    not_work_vpn = InlineKeyboardButton('Не работает VPN', callback_data='not_work_vpn')
    close_support = InlineKeyboardButton("Закрыть", callback_data="close_support")
    menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu.add(not_work_outline, not_work_vpn, close_support)
    return menu


def before_pay_menu():
    ru_pay = InlineKeyboardButton('Российский сервер 🇷🇺', callback_data='ru_pay')
    eng_pay = InlineKeyboardButton('Зарубежный сервер 🇳🇱', callback_data='eng_pay')
    support = InlineKeyboardButton('Поддержка ✌️', callback_data='support')
    close_support = InlineKeyboardButton("Закрыть", callback_data="close_support")
    menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu.add(ru_pay, eng_pay, support, close_support)
    return menu


def pay_menu(server_geo):
    mount_1 = InlineKeyboardButton('1 Месяц', callback_data=f'mount_1_{server_geo}')
    mount_3 = InlineKeyboardButton('3 Месяца', callback_data=f'mount_3_{server_geo}')
    mount_6 = InlineKeyboardButton('6 Месяцев', callback_data=f'mount_6_{server_geo}')
    mount_12 = InlineKeyboardButton('12 Месяцев', callback_data=f'mount_12_{server_geo}')
    close_support = InlineKeyboardButton("Назад", callback_data="bacK_to_before_pay")
    menu = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    menu.add(mount_1, mount_3, mount_6, mount_12)
    menu.add(close_support)
    return menu


def prolong_pay_menu():
    prolong_pay = InlineKeyboardButton('Продлить Подписку 😊', callback_data='subscribe')
