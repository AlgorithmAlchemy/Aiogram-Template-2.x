"""
Модели пользователей
"""
from peewee import (
    IntegerField, CharField, BooleanField, DateTimeField, 
    ForeignKeyField, TextField, DecimalField, DateField
)
from datetime import datetime, date
from models.base import BaseModel
from utils.db_api.sqlite import db


class User(BaseModel):
    """Модель пользователя"""
    
    # Основные поля
    user_id = IntegerField(unique=True, primary_key=True, verbose_name='ID пользователя')
    username = CharField(null=True, max_length=32, verbose_name='Username')
    first_name = CharField(max_length=64, verbose_name='Имя')
    last_name = CharField(null=True, max_length=64, verbose_name='Фамилия')
    language_code = CharField(null=True, max_length=10, verbose_name='Код языка')
    
    # Статус пользователя
    is_bot = BooleanField(default=False, verbose_name='Бот')
    is_premium = BooleanField(default=False, verbose_name='Premium')
    is_verified = BooleanField(default=False, verbose_name='Верифицирован')
    
    # Модерация
    is_banned = BooleanField(default=False, verbose_name='Забанен')
    is_muted = BooleanField(default=False, verbose_name='Замучен')
    warnings = IntegerField(default=0, verbose_name='Предупреждения')
    max_warnings = IntegerField(default=3, verbose_name='Макс предупреждений')
    
    # Дополнительная информация
    phone_number = CharField(null=True, max_length=20, verbose_name='Телефон')
    email = CharField(null=True, max_length=100, verbose_name='Email')
    birth_date = DateField(null=True, verbose_name='Дата рождения')
    bio = TextField(null=True, verbose_name='Биография')
    
    # Статистика
    last_activity = DateTimeField(default=datetime.now, verbose_name='Последняя активность')
    join_date = DateTimeField(default=datetime.now, verbose_name='Дата регистрации')
    messages_count = IntegerField(default=0, verbose_name='Количество сообщений')
    commands_count = IntegerField(default=0, verbose_name='Количество команд')
    
    # Настройки
    timezone = CharField(default='Europe/Moscow', max_length=50, verbose_name='Часовой пояс')
    notification_enabled = BooleanField(default=True, verbose_name='Уведомления включены')
    
    class Meta:
        table_name = 'users'
        indexes = (
            (('username',), False),  # Неуникальный индекс для username
            (('is_banned',), False),
            (('is_active',), False),
            (('last_activity',), False),
        )
    
    def __str__(self):
        return f"User(id={self.user_id}, username=@{self.username})"
    
    # Методы для модерации
    def is_active_user(self):
        """Проверяет, активен ли пользователь"""
        return not self.is_banned and not self.is_muted and self.is_active
    
    def can_be_warned(self):
        """Проверяет, можно ли предупредить пользователя"""
        return self.warnings < self.max_warnings
    
    def add_warning(self, reason: str = None):
        """Добавляет предупреждение"""
        if self.can_be_warned():
            self.warnings += 1
            self.save()
            
            # Создаем запись о предупреждении
            UserWarning.create(
                user=self,
                reason=reason or "Причина не указана",
                warning_number=self.warnings
            )
            
            # Автоматический бан при достижении максимума
            if self.warnings >= self.max_warnings:
                self.ban("Достигнут максимум предупреждений")
            
            return True
        return False
    
    def remove_warning(self):
        """Убирает предупреждение"""
        if self.warnings > 0:
            self.warnings -= 1
            self.save()
            return True
        return False
    
    def ban(self, reason: str = None):
        """Банит пользователя"""
        self.is_banned = True
        self.save()
        
        # Создаем запись о бане
        UserBan.create(
            user=self,
            reason=reason or "Причина не указана"
        )
    
    def unban(self):
        """Разбанивает пользователя"""
        self.is_banned = False
        self.save()
        
        # Создаем запись о разбане
        UserUnban.create(user=self)
    
    def mute(self, duration_minutes: int = None, reason: str = None):
        """Мутит пользователя"""
        self.is_muted = True
        self.save()
        
        # Создаем запись о муте
        UserMute.create(
            user=self,
            duration_minutes=duration_minutes,
            reason=reason or "Причина не указана"
        )
    
    def unmute(self):
        """Размучивает пользователя"""
        self.is_muted = False
        self.save()
        
        # Создаем запись о размуте
        UserUnmute.create(user=self)
    
    def update_activity(self):
        """Обновляет время последней активности"""
        self.last_activity = datetime.now()
        self.messages_count += 1
        self.save()
    
    def increment_commands(self):
        """Увеличивает счетчик команд"""
        self.commands_count += 1
        self.save()
    
    # Методы для получения связанных данных
    def get_settings(self):
        """Получает настройки пользователя"""
        return UserSettings.get_or_create(user=self)[0]
    
    def get_stats(self):
        """Получает статистику пользователя"""
        return UserStats.get_or_create(user=self)[0]
    
    def get_warnings_history(self):
        """Получает историю предупреждений"""
        return UserWarning.select().where(UserWarning.user == self).order_by(UserWarning.created_at.desc())
    
    def get_ban_history(self):
        """Получает историю банов"""
        return UserBan.select().where(UserBan.user == self).order_by(UserBan.created_at.desc())


class UserSettings(BaseModel):
    """Настройки пользователя"""
    
    user = ForeignKeyField(User, backref='settings', verbose_name='Пользователь')
    
    # Языковые настройки
    language = CharField(default='ru', max_length=5, verbose_name='Язык')
    date_format = CharField(default='DD.MM.YYYY', max_length=20, verbose_name='Формат даты')
    time_format = CharField(default='24h', max_length=10, verbose_name='Формат времени')
    
    # Настройки уведомлений
    notifications_enabled = BooleanField(default=True, verbose_name='Уведомления включены')
    email_notifications = BooleanField(default=False, verbose_name='Email уведомления')
    push_notifications = BooleanField(default=True, verbose_name='Push уведомления')
    
    # Настройки интерфейса
    theme = CharField(default='light', max_length=10, verbose_name='Тема')
    compact_mode = BooleanField(default=False, verbose_name='Компактный режим')
    auto_delete_messages = BooleanField(default=False, verbose_name='Автоудаление сообщений')
    
    # Приватность
    profile_visible = BooleanField(default=True, verbose_name='Профиль видим')
    show_online_status = BooleanField(default=True, verbose_name='Показывать статус')
    allow_messages = BooleanField(default=True, verbose_name='Разрешить сообщения')
    
    class Meta:
        table_name = 'user_settings'
    
    def __str__(self):
        return f"Settings for {self.user}"


class UserStats(BaseModel):
    """Статистика пользователя"""
    
    user = ForeignKeyField(User, backref='stats', verbose_name='Пользователь')
    
    # Счетчики сообщений
    messages_sent = IntegerField(default=0, verbose_name='Отправлено сообщений')
    commands_used = IntegerField(default=0, verbose_name='Использовано команд')
    files_sent = IntegerField(default=0, verbose_name='Отправлено файлов')
    
    # Счетчики медиа
    photos_sent = IntegerField(default=0, verbose_name='Отправлено фото')
    videos_sent = IntegerField(default=0, verbose_name='Отправлено видео')
    documents_sent = IntegerField(default=0, verbose_name='Отправлено документов')
    voice_messages = IntegerField(default=0, verbose_name='Голосовых сообщений')
    video_notes = IntegerField(default=0, verbose_name='Видеосообщений')
    stickers_sent = IntegerField(default=0, verbose_name='Отправлено стикеров')
    
    # Временные метки
    last_message_date = DateTimeField(null=True, verbose_name='Последнее сообщение')
    last_command_date = DateTimeField(null=True, verbose_name='Последняя команда')
    
    # Дополнительная статистика
    total_chars_sent = IntegerField(default=0, verbose_name='Всего символов')
    average_message_length = DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='Средняя длина сообщения')
    
    class Meta:
        table_name = 'user_stats'
    
    def __str__(self):
        return f"Stats for {self.user}"
    
    def increment_messages(self, message_length: int = 0):
        """Увеличивает счетчик сообщений"""
        self.messages_sent += 1
        self.total_chars_sent += message_length
        self.last_message_date = datetime.now()
        
        # Обновляем среднюю длину сообщения
        if self.messages_sent > 0:
            self.average_message_length = self.total_chars_sent / self.messages_sent
        
        self.save()
    
    def increment_commands(self):
        """Увеличивает счетчик команд"""
        self.commands_used += 1
        self.last_command_date = datetime.now()
        self.save()
    
    def increment_files(self, file_type: str = 'document'):
        """Увеличивает счетчик файлов по типу"""
        self.files_sent += 1
        
        if file_type == 'photo':
            self.photos_sent += 1
        elif file_type == 'video':
            self.videos_sent += 1
        elif file_type == 'document':
            self.documents_sent += 1
        elif file_type == 'voice':
            self.voice_messages += 1
        elif file_type == 'video_note':
            self.video_notes += 1
        elif file_type == 'sticker':
            self.stickers_sent += 1
        
        self.save()


# Модели для истории модерации
class UserWarning(BaseModel):
    """История предупреждений пользователей"""
    
    user = ForeignKeyField(User, backref='warnings_history', verbose_name='Пользователь')
    warning_number = IntegerField(verbose_name='Номер предупреждения')
    reason = TextField(verbose_name='Причина')
    moderator_id = IntegerField(null=True, verbose_name='ID модератора')
    
    class Meta:
        table_name = 'user_warnings'


class UserBan(BaseModel):
    """История банов пользователей"""
    
    user = ForeignKeyField(User, backref='bans_history', verbose_name='Пользователь')
    reason = TextField(verbose_name='Причина')
    moderator_id = IntegerField(null=True, verbose_name='ID модератора')
    duration_days = IntegerField(null=True, verbose_name='Длительность в днях')
    
    class Meta:
        table_name = 'user_bans'


class UserUnban(BaseModel):
    """История разбанов пользователей"""
    
    user = ForeignKeyField(User, backref='unbans_history', verbose_name='Пользователь')
    moderator_id = IntegerField(null=True, verbose_name='ID модератора')
    reason = TextField(null=True, verbose_name='Причина разбана')
    
    class Meta:
        table_name = 'user_unbans'


class UserMute(BaseModel):
    """История мутов пользователей"""
    
    user = ForeignKeyField(User, backref='mutes_history', verbose_name='Пользователь')
    reason = TextField(verbose_name='Причина')
    moderator_id = IntegerField(null=True, verbose_name='ID модератора')
    duration_minutes = IntegerField(null=True, verbose_name='Длительность в минутах')
    
    class Meta:
        table_name = 'user_mutes'


class UserUnmute(BaseModel):
    """История размутов пользователей"""
    
    user = ForeignKeyField(User, backref='unmutes_history', verbose_name='Пользователь')
    moderator_id = IntegerField(null=True, verbose_name='ID модератора')
    reason = TextField(null=True, verbose_name='Причина размута')
    
    class Meta:
        table_name = 'user_unmutes'
