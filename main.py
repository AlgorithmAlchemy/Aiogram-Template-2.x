from aiogram import executor
from aiogram.types import AllowedUpdates
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from data.config import ...

import sqlite3
import asyncio

from models.sqlite3_creator import db, connect
from loader import dp, bot
import filters, handlers, models, states

def your_fun():
    pass
#  ###################  ###################

async def on_startup(dp):
    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(your_fun, trigger='interval', hours=0, minutes=5, seconds=60)
    # scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, allowed_updates=AllowedUpdates.all(), on_startup=on_startup)
