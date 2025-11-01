from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_city = State()
    waiting_for_phone = State()
    waiting_for_confirmation = State()


class FeedbackStates(StatesGroup):
    waiting_for_feedback_text = State()
    waiting_for_rating = State()
    waiting_for_confirmation = State()


class SettingsStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_theme = State()
    waiting_for_notifications = State()


class SupportStates(StatesGroup):
    waiting_for_issue_type = State()
    waiting_for_description = State()
    waiting_for_contact = State()
