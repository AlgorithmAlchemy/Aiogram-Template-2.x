import asyncio
import json
from datetime import date, timedelta
import sys

from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram import types, utils
from aiogram.types import Update

from loader import dp, bot
import sqlite3
from models.sqlite3_creator import db, connect

from datetime import datetime
