"""
Базовая модель для всех таблиц
"""
from peewee import Model, DateTimeField, BooleanField
from datetime import datetime
from typing import List, Optional, Type, TypeVar, Any
from database.connection import db

T = TypeVar('T', bound='BaseModel')


class BaseModel(Model):
    """Базовая модель для всех таблиц"""

    # Общие поля для всех таблиц
    created_at: DateTimeField = DateTimeField(
        default=datetime.now, 
        verbose_name='Дата создания'
    )
    updated_at: DateTimeField = DateTimeField(
        default=datetime.now, 
        verbose_name='Дата обновления'
    )
    is_active: BooleanField = BooleanField(
        default=True, 
        verbose_name='Активен'
    )

    class Meta:
        database = db
        legacy_table_names = False  # Используем современные имена таблиц

    def save(self, *args: Any, **kwargs: Any) -> int:
        """Переопределяем save для автоматического обновления updated_at"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def get_active(cls: Type[T]) -> List[T]:
        """Получить только активные записи"""
        return list(cls.select().where(cls.is_active))

    @classmethod
    def get_inactive(cls: Type[T]) -> List[T]:
        """Получить только неактивные записи"""
        return list(cls.select().where(~cls.is_active))

    def soft_delete(self) -> None:
        """Мягкое удаление записи"""
        self.is_active = False
        self.save()

    def restore(self) -> None:
        """Восстановление записи"""
        self.is_active = True
        self.save()

    @classmethod
    def get_by_id_safe(cls: Type[T], id_value: int) -> Optional[T]:
        """Безопасное получение записи по ID"""
        try:
            return cls.get(cls.id == id_value, cls.is_active)
        except cls.DoesNotExist:
            return None

    @classmethod
    def exists_active(cls: Type[T], id_value: int) -> bool:
        """Проверка существования активной записи"""
        return cls.select().where(
            cls.id == id_value, 
            cls.is_active
        ).exists()
    
    def __str__(self):
        """Строковое представление модели"""
        return f"{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})"
    
    def __repr__(self):
        """Представление для отладки"""
        return self.__str__()
