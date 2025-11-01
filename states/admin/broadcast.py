from aiogram.dispatcher.filters.state import State, StatesGroup


class BroadcastStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()
    waiting_for_target = State()  # all, users, admins


class UserManagementStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_action = State()  # ban, unban, warn
    waiting_for_reason = State()
    waiting_for_confirmation = State()


class BackupStates(StatesGroup):
    waiting_for_backup_type = State()  # full, users, settings
    waiting_for_confirmation = State()
