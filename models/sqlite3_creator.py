import sqlite3


# b_option = top secret auto back-up
db = sqlite3.connect('users.sqlite')
connect = db.cursor()
connect.execute('''CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  chat_id TEXT,
  bot_message_language TEXT,
  language_code TEXT,                                       
  message_id TEXT,

  is_bot TEXT,
  first_name TEXT,
  username TEXT,
  role TEXT,

  text TEXT,
  type TEXT,
  balance FLOAT,
  reg_date TEXT,
  orders INTEGER,
  first_start TEXT,
  subscribe_status TEXT,
  subscribe_day INTEGER,
  subscribe_time_start TEXT,
  subscribe_time_seconds INTEGER,
  terms_of_use INTEGER,
  demo_or_full TEXT,
  vpn_strings TEXT,
  vpn_country TEXT,
  subscribe_activate_data TEXT,
  subscribe_deactivate_data TEXT,
  
  user_timer_checker_status_code INTEGER DEFAULT 0,
  UNIQUE (chat_id)
)''')

# status_use_or_not 0 = not use
# status_ban_or_not 0 = not ban

# user_timer_checker_status_code = идём от 0 и выше по статусам уведомлений юзера

# таблица с демо доступами
connect.execute('''CREATE TABLE IF NOT EXISTS region_3d (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  finland TEXT,
  kazakhstan TEXT,
  germany TEXT,
  austria TEXT,
  russia TEXT,
  india TEXT,
  netherlands TEXT,
  usa TEXT,
  status_use_or_not TEXT DEFAULT 0,
  status_ban_or_not TEXT DEFAULT 0,
  user_id TEXT,
  UNIQUE (finland, kazakhstan, germany, austria, russia, india, netherlands, usa)
)''')

# таблица с доступами на 1 месяц
connect.execute('''CREATE TABLE IF NOT EXISTS region_1m (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  finland TEXT,
  kazakhstan TEXT,
  germany TEXT,
  austria TEXT,
  russia TEXT,
  india TEXT,
  netherlands TEXT,
  usa TEXT,
  status_use_or_not TEXT DEFAULT 0,
  status_ban_or_not TEXT DEFAULT 0,
  user_id TEXT,
  UNIQUE (finland, kazakhstan, germany, austria, russia, india, netherlands, usa)
)''')

# таблица с доступами на 3 месяц
connect.execute('''CREATE TABLE IF NOT EXISTS region_3m (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  finland TEXT,
  kazakhstan TEXT,
  germany TEXT,
  austria TEXT,
  russia TEXT,
  india TEXT,
  netherlands TEXT,
  usa TEXT,
  status_use_or_not TEXT DEFAULT 0,
  status_ban_or_not TEXT DEFAULT 0,
  user_id TEXT,
  UNIQUE (finland, kazakhstan, germany, austria, russia, india, netherlands, usa)
)''')

# таблица с доступами на 6 месяц
connect.execute('''CREATE TABLE IF NOT EXISTS region_6m (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  finland TEXT,
  kazakhstan TEXT,
  germany TEXT,
  austria TEXT,
  russia TEXT,
  india TEXT,
  netherlands TEXT,
  usa TEXT,
  status_use_or_not TEXT DEFAULT 0,
  status_ban_or_not TEXT DEFAULT 0,
  user_id TEXT,
  UNIQUE (finland, kazakhstan, germany, austria, russia, india, netherlands, usa)
)''')

# таблица с доступами на 12 месяц
connect.execute('''CREATE TABLE IF NOT EXISTS region_12m (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  finland TEXT,
  kazakhstan TEXT,
  germany TEXT,
  austria TEXT,
  russia TEXT,
  india TEXT,
  netherlands TEXT,
  usa TEXT,
  status_use_or_not TEXT DEFAULT 0,
  status_ban_or_not TEXT DEFAULT 0,
  user_id TEXT,
  UNIQUE (finland, kazakhstan, germany, austria, russia, india, netherlands, usa)
)''')


connect.execute('''CREATE TABLE IF NOT EXISTS invoice (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  message_id  TEXT,
  status TEXT DEFAULT 0
)''')