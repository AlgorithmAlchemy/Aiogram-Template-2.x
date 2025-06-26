from peewee import *

path_to_db = "data/botBD.db"

db = SqliteDatabase(path_to_db)
db.connect()
