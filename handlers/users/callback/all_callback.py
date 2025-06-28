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

