"""
Базовые модели для базы данных
"""
from peewee import Model, DateTimeField, BooleanField
from datetime import datetime
from database.connection import db


class BaseModel(Model):
    """Базовая модель для всех таблиц"""
    
    # Общие поля для всех таблиц
    created_at = DateTimeField(default=datetime.now, verbose_name='Дата создания')
    updated_at = DateTimeField(default=datetime.now, verbose_name='Дата обновления')
    is_active = BooleanField(default=True, verbose_name='Активен')
    
    class Meta:
        database = db
        legacy_table_names = False  # Используем современные имена таблиц
    
    def save(self, *args, **kwargs):
        """Переопределяем save для автоматического обновления updated_at"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_active(cls):
        """Получить только активные записи"""
        return cls.select().where(cls.is_active == True)
    
    @classmethod
    def get_inactive(cls):
        """Получить только неактивные записи"""
        return cls.select().where(cls.is_active == False)
    
    def soft_delete(self):
        """Мягкое удаление записи"""
        self.is_active = False
        self.save()
    
    def restore(self):
        """Восстановление записи"""
        self.is_active = True
        self.save()
    
    def __str__(self):
        """Строковое представление модели"""
        return f"{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})"
    
    def __repr__(self):
        """Представление для отладки"""
        return self.__str__()
