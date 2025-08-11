from peewee import (
    Model, IntegerField, CharField, BooleanField, 
    DateTimeField, ForeignKeyField
)
from datetime import datetime
from utils.db_api.sqlite import db


class User(Model):
    """Модель пользователя"""
    user_id = IntegerField(unique=True, primary_key=True)
    username = CharField(null=True, max_length=32)
    first_name = CharField(max_length=64)
    last_name = CharField(null=True, max_length=64)
    language_code = CharField(null=True, max_length=10)
    is_bot = BooleanField(default=False)
    is_premium = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    is_banned = BooleanField(default=False)
    is_muted = BooleanField(default=False)
    warnings = IntegerField(default=0)
    max_warnings = IntegerField(default=3)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    last_activity = DateTimeField(default=datetime.now)
    join_date = DateTimeField(default=datetime.now)
    
    class Meta:
        database = db
        table_name = 'users'
    
    def __str__(self):
        return f"User(id={self.user_id}, username=@{self.username})"
    
    def is_active(self):
        """Проверяет, активен ли пользователь"""
        return not self.is_banned and not self.is_muted
    
    def can_be_warned(self):
        """Проверяет, можно ли предупредить пользователя"""
        return self.warnings < self.max_warnings
    
    def add_warning(self):
        """Добавляет предупреждение"""
        if self.can_be_warned():
            self.warnings += 1
            self.save()
            return True
        return False
    
    def remove_warning(self):
        """Убирает предупреждение"""
        if self.warnings > 0:
            self.warnings -= 1
            self.save()
            return True
        return False
    
    def ban(self):
        """Банит пользователя"""
        self.is_banned = True
        self.save()
    
    def unban(self):
        """Разбанивает пользователя"""
        self.is_banned = False
        self.save()
    
    def mute(self):
        """Мутит пользователя"""
        self.is_muted = True
        self.save()
    
    def unmute(self):
        """Размучивает пользователя"""
        self.is_muted = False
        self.save()
    
    def update_activity(self):
        """Обновляет время последней активности"""
        self.last_activity = datetime.now()
        self.save()


class UserSettings(Model):
    """Настройки пользователя"""
    user = ForeignKeyField(User, backref='settings')
    language = CharField(default='ru', max_length=5)
    notifications = BooleanField(default=True)
    auto_delete = BooleanField(default=False)
    theme = CharField(default='light', max_length=10)
    timezone = CharField(default='Europe/Moscow', max_length=50)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = db
        table_name = 'user_settings'
    
    def __str__(self):
        return f"Settings for {self.user}"


class UserStats(Model):
    """Статистика пользователя"""
    user = ForeignKeyField(User, backref='stats')
    messages_sent = IntegerField(default=0)
    commands_used = IntegerField(default=0)
    files_sent = IntegerField(default=0)
    photos_sent = IntegerField(default=0)
    videos_sent = IntegerField(default=0)
    documents_sent = IntegerField(default=0)
    voice_messages = IntegerField(default=0)
    video_notes = IntegerField(default=0)
    stickers_sent = IntegerField(default=0)
    last_message_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = db
        table_name = 'user_stats'
    
    def __str__(self):
        return f"Stats for {self.user}"
    
    def increment_messages(self):
        """Увеличивает счетчик сообщений"""
        self.messages_sent += 1
        self.last_message_date = datetime.now()
        self.save()
    
    def increment_commands(self):
        """Увеличивает счетчик команд"""
        self.commands_used += 1
        self.save()
    
    def increment_files(self):
        """Увеличивает счетчик файлов"""
        self.files_sent += 1
        self.save()
    
    def increment_photos(self):
        """Увеличивает счетчик фото"""
        self.photos_sent += 1
        self.save()
    
    def increment_videos(self):
        """Увеличивает счетчик видео"""
        self.videos_sent += 1
        self.save()
    
    def increment_documents(self):
        """Увеличивает счетчик документов"""
        self.documents_sent += 1
        self.save()
    
    def increment_voice(self):
        """Увеличивает счетчик голосовых сообщений"""
        self.voice_messages += 1
        self.save()
    
    def increment_video_notes(self):
        """Увеличивает счетчик видео-заметок"""
        self.video_notes += 1
        self.save()
    
    def increment_stickers(self):
        """Увеличивает счетчик стикеров"""
        self.stickers_sent += 1
        self.save()
