import datetime

from aiogram.utils.markdown import text, link

OWNER = ['6251140356', '451658425', '319869370', '5567421624']
CHAT = -1001826136461
SUPPORT = '@localvpn_support'


API_TOKEN = '6270008866:AAEpDh88HLSJSyz1qaT_KJx12YnVv4m4M8E'      # local vpn
# API_TOKEN = '6450308672:AAFQFhsA2xqmvW_6DiKtlPtbtOXOCJieSaU'        # py test

demo_day_counter = 3

# ----------
# Start Message
username = "User"
hello_ru = f'''Салют, {username}! Это Local VPN⚡️

Пользуясь нашим сервисом Вы точно забудете про низкую скорость, мешающую рекламу и постоянные включения и отключения VPN-а. 
Продолжая, вы автоматически принимаете условия данного Пользовательского соглашения ...?

Нажмите кнопку «Подключить VPN», чтобы открыть меню и получить дальнейшие инструкции.

'''

hello_en = f'''Salute, {username}! This is Local VPN⚡️

Using our service you will definitely forget about the low speed, interfering advertising and constant inclusions and disconnections of the VPN. 
By continuing, you automatically accept the terms of this User Agreement...?

Click the "Connect VPN" button to open the menu and get further instructions.

'''

# ----------
main_menu_ru = f'''Главное меню

⚡️ Демо доступ активирован!
Дней осталось: 3


- Для выбора региона и получения подробной инструкции по установке VPN на всех ваших устройствах воспользуйтесь кнопками меню.

'''

# ----------
admin_help_ru = text(f"<b>Все команды бота (Users):</b>"
                     f"\n/start <code>- Основное меню бота</code>"
                     f"\n/help <code>- Сапорт</code>"
                     f"\n/lang <code>- Смена языка</code>"

                     f"\n\n<b>Все команды бота (Owner):</b>"
                     f"\n/add_category <code>- добавляет товарную категорию</code>"
                     f"\n/de_category <code>- деактивируем категорию</code>"
                     f"\n/activate <code>- активируем категорию</code>"
                     f"\n/category <code>- доступные категории и их id</code>"
                     f"\n\n/upload - <code>загрузка товара</code>"
                     f"\n\n/add_balance <code>- добавляем баланс юзеру в долларах /add_balance $id$100</code>"

                     f"\n\n\n/export <code>- Экспортируем все User.id пользователей бота</code>"
                     f"\n/stat <code>- Статистика бота</code>"

                     f"\n\n/share <code>- Отправить пост в все группы</code>"
                     f"\n/share_ch <code>- Отправть пост в все каналы</code>"
                     f"\n/share_all <code>- Отправляет в все группы и каналы</code>"
                     f"\n/send_users <code>- Отправить пост всем пользователям</code>"
                     f"\n/send_one <code>- Отправляет сообщение пользователю</code>"
                     f"\n/drop_list <code>- Показывает все каналы и чаты в которые добавлен бот</code>")

admin_help_en = text(f"<b>All bot commands (Users):</b>"
                     f"\n/start <code>- Bot main menu</code>"
                     f"\n/help <code>- Help</code>"
                     f"\n/lang <code>- Change language</code>"

                     f"\n\n<b>All bot commands (Owner):</b>"
                     f"\n/add_category <code>- adds a product category</code>"
                     f"\n/de_category <code>- deactivate category</code>"
                     f"\n/activate <code>- activate the category</code>"
                     f"\n/category <code>- available categories and their id</code>"
                     f"\n\n/upload - <code>upload product</code>"
                     f"\n\n/add_balance <code>- add balance to user in dollars /add_balance $id$100</code>"

                     f"\n\n\n/export <code>- Export all User.id of bot users</code>"
                     f"\n/stat <code>- Bot statistics</code>"
                     f"\n\n/share <code>- Send post to all groups</code>"
                     f"\n/share_ch <code>- Share post to all channels</code>"
                     f"\n/share_all <code>- Sends to all groups and channels</code>"
                     f"\n/send_users <code>- Send post to all users</code>"
                     f"\n/send_one <code>- Sends a message to the user</code>"
                     f"\n/drop_list <code>- Shows all channels and chats where the bot has been added</code>")


# ----------

def generate_demo_message(link, day_counter):
    return f'''
Пробный период активирован!

Осталось дней: {day_counter}. 

Для подключения VPN и получения подробной инструкции по установке воспользуйтесь кнопками меню.
'''


send_message_pre_demo_menu = f'Первый шаг сделан и мы дарим Вам 3 дня пробного периода!' \
                             f'\n\nИли можно подключить полную подписку,воспользовавшись кнопкой меню.'

"""demo_menu_message = f'Мы стали ещё ближе...' \
                    f'\n\n\n' \
                    f'⚡️<u>Демо доступ активирован!</u>' \
                    f'\nДней осталось: days_counter д.' \
                    f'\n\n\nДля выбора региона и получения подробной' \
                    f'\nинструкции по установке VPN на всех ваших ' \
                    f'\nустройствах воспользуйтесь кнопками меню.' \
                    f'\n\n-Для получения полного доступа продлите ' \
                    f'\nподписку.'"""

demo_menu_message = f'''
Первый шаг сделан и мы дарим Вам 3 дня пробного периода на зарубежном сервере! 

Нажмите “Получить пробный период”  и следуйте дальнейшим инструкциям.

Или выберите полный доступ и подключите зарубежный или российский VPN на необходимый Вам срок.

'''

demo_region_message_11 = f'''
Выбор региона

Для демо доступа вам доступны следующие зоны:
🇳🇱 Нидерланды

- Для настройки VPN нажмите название региона и следуйте инструкциям на экране
- Для того чтобы получить доступ ко всем регионам, оплатите подписку.

'''

one_step_confirm = f'Первый шаг сделан и мы дарим Вам 3 дня пробного периода!' \
                   f'\n\nИли можно подключить полную подписку,воспользовавшись кнопкой меню.'

full_access_message = '''<b>Отлично, Вы выбрали подключение полного доступа!</b>

Какой VPN Вам необходим:
зарубежный или российский?
'''


def data():
    parse_date = str(datetime.datetime.now().date()).replace("datetime.date", "").replace("(", "").replace(")", "")
    parse_time = str(datetime.datetime.now().time()).split(".")
    parse_time = parse_time[0]
    return parse_time + parse_date


# ----------
# Help message
help_rus = text(f"⭐️Возможно, я смогу тебе чем-то помочь.",
                f"\n📞Связь: {SUPPORT}",
                f"\n🏠Домой: /start")

help_eng = text("⭐️Perhaps I can help you with something.",
                f"\n📞Communication: @traficmaker",
                # "\n🌐Change language: /lang",
                "\n🏠Home: /start")
