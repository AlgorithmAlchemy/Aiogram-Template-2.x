import asyncio
import json
from datetime import date, timedelta
import sys

from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram import types, utils
from aiogram.types import Update

from loader import dp, bot
import sqlite3
from data.config import demo_menu_message, one_step_confirm, data, \
    demo_day_counter, full_access_message, generate_demo_message, CHAT
from keyboards.inline import home_menu, terms_of_use_menu, main_menu_limited_access, \
    region_selection_menu, support_menu, pay_menu, before_pay_menu
from models.sqlite3_creator import db, connect

from datetime import datetime


# Реагируем на быстрое подключение
@dp.callback_query_handler(text=r'get_free_time')
async def drop_video_id(call: types.CallbackQuery):
    message_id = call.message.message_id  # Идентификатор сообщения для редактирования
    chat_id = call.message.chat.id

    activate_date = data()[0]
    print(activate_date)
    query = f"SELECT netherlands FROM region_3d WHERE status_use_or_not = 0 AND status_ban_or_not = 0"
    connect.execute(query)
    result = connect.fetchone()

    print(result)

    if result is not None:
        netherlands = result[0]
        print(netherlands, '37 string all callback')
        # Дальнейшая обработка значения netherlands

        # Теперь выполните UPDATE, чтобы изменить status_use_or_not
        query_update = "UPDATE region_3d SET status_use_or_not = 1, user_id = ? WHERE netherlands = ?"
        connect.execute(query_update, (chat_id, netherlands))
        db.commit()

        # Дальнейшая обработка полученного значения netherlands
    else:
        await bot.send_message(chat_id=CHAT, text=f'Нет доступных vpn-строк! \nДней: 3\nГео: netherlands')
        await call.answer(show_alert=True, text='Нет доступных серверов, повторите попытку позже!')
        return

    activate_date = data()
    demo_seconds_counter = demo_day_counter * 24 * 60 * 60
    query = "UPDATE users SET subscribe_status = ?, subscribe_day = ?, subscribe_time_start = ?, demo_or_full = ?," \
            " subscribe_time_seconds = ?, vpn_strings = ? WHERE user_id = ?"
    connect.execute(query, ('active', demo_day_counter, activate_date, 'demo', demo_seconds_counter, netherlands,
                            chat_id,))
    db.commit()

    with open('image_3.png', 'rb') as photo:
        media = types.InputMediaPhoto(media=photo)

        demo_message = generate_demo_message(netherlands, demo_day_counter)

        await call.message.edit_media(media=media, reply_markup=home_menu('demo_activate', netherlands))
        await call.message.edit_caption(caption=str(demo_message),
                                        parse_mode='HTML', reply_markup=home_menu('demo_activate',
                                                                                  netherlands))


# Реагируем на кнопку подключит впн
@dp.callback_query_handler(regexp=r'accept_terms_of_use')
async def drop_video_id(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    activate_date = data()

    query = "UPDATE users SET first_start = ?, terms_of_use = ? WHERE user_id = ?"
    connect.execute(query, (1, 1, chat_id,))
    db.commit()

    await call.message.delete()

    with open('image_one.png', 'rb') as photo:
        await bot.send_photo(chat_id, photo, caption=demo_menu_message,
                             parse_mode='HTML',
                             reply_markup=home_menu('pre_demo'))


# Реагируем на быстрое подключение
@dp.callback_query_handler(regexp=r'fast_connect')
async def drop_video_id(call: types.CallbackQuery):
    message_id = call.message.message_id  # Идентификатор сообщения для редактирования
    chat_id = call.message.chat.id

    query = '''SELECT subscribe_time, demo_or_full FROM users WHERE user_id = ?'''
    parameters = (chat_id,)

    cursor = db.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchone()

    subscribe_time = result[0]
    demo_or_full = result[1]

    with open('image_one.png', 'rb') as photo:
        await bot.edit_message_caption(chat_id, message_id, photo, caption='dddd', parse_mode='HTML',
                                       reply_markup=region_selection_menu(demo_or_full=demo_or_full, access_days=0))


# меню для подключения подписки
@dp.callback_query_handler(regexp=r'subscription_management')
async def drop_video_id(call: types.CallbackQuery):
    await call.answer('тут платежку выбиваем')


# меню для подключения подписки
@dp.callback_query_handler(regexp=r'not_work_vpn')
async def drop_video_id(call: types.CallbackQuery):
    await call.message.edit_text('''Поддержка

Решение:
Попробуйте отключиться от сервера, закрыть приложение и запустить заново. Подключитесь к выбранному серверу.
    ''', reply_markup=support_menu())


# меню для подключения подписки
@dp.callback_query_handler(regexp=r'not_work_outline')
async def drop_video_id(call: types.CallbackQuery):
    await call.message.edit_text(''' Поддержка

Решение:
Если у вас не работает интернет, попробуйте отключить VPN в приложении Outline. Если соединение с Интернетом восстановится - подключитесь заново и продолжайте работу. ''',
                                 reply_markup=support_menu())


# меню для подключения подписки
@dp.callback_query_handler(regexp=r'close_support')
async def drop_video_id(call: types.CallbackQuery):
    await call.message.delete()


# меню для подключения подписки
@dp.callback_query_handler(regexp=r'subscribe')
async def drop_video_id(call: types.CallbackQuery):
    await call.message.answer(text=full_access_message, reply_markup=before_pay_menu(), parse_mode='HTML')


@dp.callback_query_handler(regexp=r'bacK_to_before_pay')
async def drop_video_id(call: types.CallbackQuery):
    await call.message.edit_text(text=full_access_message, reply_markup=before_pay_menu(), parse_mode='HTML')


@dp.callback_query_handler(regexp=r'ru_pay')
async def drop_video_id(call: types.CallbackQuery):
    pay_message = ''' 
Российский сервер 🇷🇺

Выберите удобный для Вас срок пользования:

1 месяц - 299 руб.
3 месяц - 699 руб.
6 месяц - 1299 руб.
12 месяц - 2 299 руб.

Оплата происходит любой удобной картой РФ: МИР,  Visa, MasterCard  💳
    '''
    await call.message.edit_text(text=pay_message, reply_markup=pay_menu("ru"), parse_mode='HTML')


@dp.callback_query_handler(regexp=r'eng_pay')
async def drop_video_id(call: types.CallbackQuery):
    pay_message = ''' 
Зарубежный сервер 🇳🇱

Выберите удобный для Вас срок пользования:

1 месяц - 299 руб.
3 месяц - 699 руб.
6 месяц - 1299 руб.
12 месяц - 2 299 руб.

Оплата происходит любой удобной картой РФ: МИР,  Visa, MasterCard  💳
    '''
    await call.message.edit_text(text=pay_message, reply_markup=pay_menu("net"), parse_mode='HTML')


@dp.callback_query_handler(regexp=r'instructions')
async def drop_video_id(call: types.CallbackQuery):
    await call.answer('РАЗРАБОТКА')
    return

    chat_id = call.message.chat.id
    query = '''SELECT subscribe_time, demo_or_full FROM users WHERE user_id = ?'''
    parameters = (chat_id,)

    cursor = db.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchone()

    subscribe_time = result[0]
    demo_or_full = result[1]

    instructions_message = ''' Подключение к VPN происходит при помощи протокола Outline. 

Для доступа к данному протоколу вам потребуется скачать приложение Outline в App Store.
Внутри бота вы получаете ключи доступа к серверам Free Surfer VPN. Каждому ключу соответствует свой регион.
Установка Outline и добавление ключей происходят в автоматическом режиме и занимают не более 1 минуты.
Всё что от вас потребуется - нажать на кнопку с названием нужной вам страны и следовать инструкциям на экране устройства.
Дальнейшее управление подключением происходит внутри приложения Outline.
Там вы сможете включать и выключать VPN, а так же менять регион.
Для большего удобства мы подготовили видео инструкции для каждой операционной системы:


    '''

    await bot.send_message(chat_id, text=one_step_confirm, parse_mode='HTML',
                           reply_markup=home_menu(demo_or_full=demo_or_full))


@dp.callback_query_handler(regexp=r'support')
async def drop_video_id(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    query = '''SELECT demo_or_full FROM users WHERE user_id = ?'''
    parameters = (chat_id,)

    cursor = db.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchone()

    support_message = '''Поддержка
    
Выберите вопрос из списка для получения
рекомендаций или свяжитесь с администрацией @localvpn_support.
    '''

    await bot.send_message(chat_id, text=support_message, parse_mode='HTML',
                           reply_markup=support_menu())


@dp.callback_query_handler(regexp=r'back_region_menu')
async def drop_video_id(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.message.from_user.id

    query = '''SELECT subscribe_time, demo_or_full FROM users WHERE user_id = ?'''
    parameters = (chat_id,)

    cursor = db.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchone()

    subscribe_time = result[0]
    demo_or_full = result[1]

    with open('image_one.png', 'rb') as photo:
        await bot.edit_message_caption(chat_id, call.message.message_id, photo,
                                       caption=demo_menu_message.replace('days_counter', str(subscribe_time)),
                                       parse_mode='HTML',
                                       reply_markup=home_menu(demo_or_full))


# ####################### подключение #######################
@dp.callback_query_handler(regexp=r'netherlands')
async def drop_video_id(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    query = '''SELECT subscribe_time, demo_or_full FROM users WHERE user_id = ?'''
    parameters = (chat_id,)

    cursor = db.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchone()

    subscribe_time = result[0]
    demo_or_full = result[1]

    if subscribe_time != 0:
        await call.answer(show_alert=True, text='Подписка закончилась!')
        return

    if demo_or_full == 'demo':
        db.execute(f''' SELECT vpn_strings FROM users WHERE user_id = {chat_id} ''')


# Callback-функция для обработки нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data.startswith('mount'))
async def process_callback_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    months = int(callback_query.data.split('_')[1])
    server_geo = callback_query.data.split('_')[2]

    if server_geo == "net":
        server_geo = "netherlands"
    if server_geo == "ru":
        server_geo = "russia"

    query = f"SELECT {server_geo} FROM region_{months}m WHERE status_use_or_not = 0 AND status_ban_or_not = 0"
    connect.execute(query)
    result = connect.fetchone()

    print(result)

    try:
        if result[0] is not None and result[0] != 'None':
            vpn_server = result[0]
            print(vpn_server)
            # Дальнейшая обработка значения netherlands

            # Теперь выполните UPDATE, чтобы изменить status_use_or_not
            # query_update = f"UPDATE region_{months}m SET status_use_or_not = 1, user_id = ? WHERE {server_geo} = ?"
            # connect.execute(query_update, (user_id, vpn_server))
            # db.commit()

            # Дальнейшая обработка полученного значения netherlands
        else:
            await bot.send_message(chat_id=CHAT, text=f'Нет доступных vpn-строк! \nМесяцев: {months}\nГео: {server_geo}')
            await callback_query.answer(show_alert=True, text='Нет доступных серверов, повторите попытку позже!')
            return

    except Exception as e:
        # Обрабатываем остальные ошибки
        print(user_id, f"Произошла ошибка: {str(e)}")

        await bot.send_message(chat_id=CHAT, text=f'Нет доступных vpn-строк! \nМесяцев: {months}\nГео: {server_geo}')
        await callback_query.answer(show_alert=True, text='Нет доступных серверов, повторите попытку позже!')

        return

    # Создание инвойса
    invoice_amount = calculate_invoice_amount(months)
    invoice_text = f"Оплата подписки на {months} месяцев: {invoice_amount} руб."

    payload_value = f"subscription_{months}_{server_geo}"  # Например, "subscription_3" для 3 месяцев

    # Отправка инвойса
    mes = await bot.send_invoice(
        chat_id=user_id,
        title=f"Подписка на {months} месяцев",
        description=invoice_text,
        payload=payload_value,
        provider_token="390540012:LIVE:38893",  # Токен вашего платежного провайдера
        # provider_token="381764678:TEST:63864",
        currency="RUB",
        prices=[types.LabeledPrice(label=f"Подписка на {months} месяцев", amount=invoice_amount * 100)]
    )

    cursor = db.cursor()

    data_to_insert = [
        (user_id, message_id),
        (mes.chat.id, mes.message_id)
    ]

    cursor.executemany('''
        INSERT INTO invoice (user_id, message_id) VALUES (?, ?)
    ''', data_to_insert)

    db.commit()


# Функция для расчета стоимости подписки
def calculate_invoice_amount(months):
    if months == 1:
        return 299
    elif months == 3:
        return 699
    elif months == 6:
        return 1299
    elif months == 12:
        return 2299
    else:
        return 0


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query)
    cursor = db.cursor()

    await bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True
    )

    user_id = pre_checkout_query.from_user.id

    # Выборка user_id и message_id с status не равным 1
    cursor.execute(f'''
        SELECT user_id, message_id
        FROM invoice
        WHERE status <> 1 AND user_id == {user_id}
    ''')

    rows = cursor.fetchall()

    for i in rows:
        print(i[0], i[1])
        try:
            await bot.delete_message(i[0], i[1])
        except MessageToDeleteNotFound:
            pass

        query = "UPDATE invoice SET status = ?"
        connect.execute(query, (1,))
        db.commit()

    print(pre_checkout_query.invoice_payload)   # subscription_1_russia

    months = int(pre_checkout_query.invoice_payload.split('_')[1])
    server_geo = str(pre_checkout_query.invoice_payload.split('_')[2])
    invoice_amount = calculate_invoice_amount(months)

    # Здесь вы можете выполнить дополнительные действия после успешной оплаты,
    # например, обновить статус пользователя в базе данных или отправить уведомление.

    await bot.send_message(
        user_id,
        "Спасибо за оплату! Ваша подписка активирована."
    )

    # даём впн строку
    query = f"SELECT {server_geo} FROM region_{months}m WHERE status_use_or_not = 0 AND status_ban_or_not = 0"
    connect.execute(query)
    result = connect.fetchone()

    print(result)

    if result[0] is not None and result[0] != 'None':
        vpn_server = result[0]
        print('vpn server', vpn_server)
        query_update = f"UPDATE region_{months}m SET status_use_or_not = 1, user_id = ? WHERE {server_geo} = ?"
        connect.execute(query_update, (user_id, vpn_server))
        db.commit()

    else:
        await bot.send_message(chat_id=CHAT, text=f'Закончились сервера, после оплаты у {user_id} на {months} месяцев')
        await bot.send_message(chat_id=user_id, show_alert=True,
                               text='К сожалению сервера закончились, сообщите администратору!')
        return

    #   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   ##   #

    seconds_counter = int(months * 30 * 24 * 60 * 60)
    subscribe_day = int(months * 30)
    activate_date = data()

    query = "UPDATE users SET subscribe_status = ?, subscribe_day = ?, subscribe_time_start = ?, demo_or_full = ?," \
            " subscribe_time_seconds = ?, vpn_strings = ? WHERE user_id = ?"
    connect.execute(query, ('active', subscribe_day, activate_date, 'full', seconds_counter, vpn_server,
                            user_id,))
    db.commit()

    #
    #
    #

    demo_message = generate_demo_message(vpn_server, subscribe_day)

    with open('image_3.png', 'rb') as photo:
        await bot.send_photo(user_id, photo, caption=demo_message.replace('Пробный период активирован!', ''),
                             parse_mode='HTML',
                             reply_markup=home_menu(demo_or_full='full', link=vpn_server))