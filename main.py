from aiogram import executor
from aiogram.types import AllowedUpdates
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import CHAT, data
from keyboards.inline import prolong_pay_menu, home_menu, prolong_24_sub

import sqlite3
import asyncio

from models.sqlite3_creator import db, connect
from loader import dp, bot
import filters, handlers, models, states


async def subscribe_day_checker():
    def update_user_status(user_id, new_status):
        update_query = "UPDATE users SET user_timer_checker_status_code = ? WHERE user_id = ?"
        connect.execute(update_query, (new_status, str(user_id)))
        db.commit()

    import datetime
    current_time = datetime.datetime.now()
    print(data(), current_time)
    query = ("SELECT user_id, subscribe_status, subscribe_day, subscribe_time_start, subscribe_time_seconds,"
             " demo_or_full, vpn_strings, subscribe_activate_data, subscribe_deactivate_data, "
             "user_timer_checker_status_code FROM users")

    # Создание подключения к базе данных внутри контекстного менеджера
    connect.execute(query)
    result = connect.fetchall()

    from datetime import datetime
    for row in result:
        print(row)
        (user_id, subscribe_status, subscribe_day, subscribe_time_start_str, subscribe_time_seconds, demo_or_full,
         vpn_strings, subscribe_activate_data, subscribe_deactivate_data, user_timer_checker_status_code) = row

        if subscribe_status != 'active':
            continue

        # Разбиваем строку времени начала подписки на части
        subscribe_time_start = datetime.strptime(subscribe_time_start_str, '%H:%M:%S %Y-%m-%d')

        # Вычисляем разницу во времени между текущим временем и временем начала подписки
        time_difference = current_time - subscribe_time_start

        # Получаем оставшиеся секунды подписки
        remaining_seconds = subscribe_time_seconds - time_difference.total_seconds()

        # Переводим секунды в дни с остатком
        subscribe_full_day = remaining_seconds / (60 * 60 * 24)

        # Получаем оставшиеся минуты подписки
        remaining_minutes = int(remaining_seconds / 60)

        # дни
        subscribe_day_new = round(subscribe_full_day)

        #
        #

        print(remaining_minutes)
        print(remaining_minutes, subscribe_full_day / 60)

        print(
            f'subscribe_day: {subscribe_day_new} / old: {subscribe_day}, type: {type(subscribe_day_new)}/{type(subscribe_day)}')
        print(f'subscribe_minutes: {remaining_minutes}')

        if subscribe_day > subscribe_day_new:  # обновляем остаток дней
            update_query = "UPDATE users SET subscribe_day = ? WHERE user_id = ?"
            connect.execute(update_query, (subscribe_day_new, str(user_id)))
            db.commit()

        if remaining_minutes < 1440 and user_timer_checker_status_code == 0:  # 1440 минут в сутках (60 минут * 24 часа)
            await bot.send_message(user_id, text='Это было классное время...'
                                                 '\n\n'
                                                 'Но до окончания действия vpn остаётся 24 часа 😢',
                                   parse_mode='HTML', reply_markup=prolong_24_sub())

            update_user_status(user_id, 1)

        elif remaining_minutes < 15 and user_timer_checker_status_code == 1:
            await bot.send_message(chat_id=CHAT, text=f'15 минут до окончания подписки {user_id}: '
                                                      f'<code>{vpn_strings}</code>')
            await bot.send_message(user_id, text='Осталось менее 15 минут до окончания подписки.',
                                   parse_mode='HTML')
            update_user_status(user_id, 2)

        elif remaining_minutes <= 0 and user_timer_checker_status_code == 2:
            end_text = (f'Нам очень жаль, но Ваша подписка закончилась...\n\n\nЧтобы продолжить'
                        f' пользоваться интернетом без границ, пожалуйста продлите подписку.')

            with open('image_two.png', 'rb') as photo:
                await bot.send_photo(user_id, photo, caption='Подписка закончилась, можете её продлить',
                                     parse_mode='HTML',
                                     reply_markup=home_menu('ended'))
            update_user_status(user_id, 3)

            query = "UPDATE users SET subscribe_status = ?, subscribe_day = ?, demo_or_full = ?," \
                    " subscribe_time_seconds = ?, vpn_strings = ?, user_timer_checker_status_code = ? WHERE user_id = ?"
            connect.execute(query, ('ended', 0, 'ended', 0, 0, 0, user_id,))
            db.commit()


async def send_message_after_20_days(user_id):
    message = "Прошло 20 дней с момента вашей регистрации. Как вам наш сервис?"

    # Отправка сообщения пользователю
    await bot.send_message(chat_id=user_id, text=message)


async def send_message_once_per_month(user_id):
    message = "Прошел месяц с момента вашей регистрации. У нас есть новые предложения для вас. Посмотрите их!"

    # Отправка сообщения пользователю
    await bot.send_message(chat_id=user_id, text=message)


#  ###################  ###################

async def on_startup(dp):
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(subscribe_day_checker, trigger='interval', hours=0, minutes=5, seconds=60)
    scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, allowed_updates=AllowedUpdates.all(), on_startup=on_startup)
