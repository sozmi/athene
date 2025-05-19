"""
Файл содержит описание моделей БД
"""
import datetime
from typing import Optional, List, Text

from sqlalchemy import ForeignKeyConstraint
from sqlmodel import SQLModel, Field, Relationship


class Image(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={'comment': 'Идентификатор изображения'})
    lid: Optional[int] = Field(foreign_key='label.id', sa_column_kwargs={'comment': 'Идентификатор метки'})
    load_date: datetime.datetime = datetime.datetime.now()
    path: str = Field(sa_column_kwargs={'comment': 'Относительный путь к изображению'})
    verify: bool = Field(sa_column_kwargs={'comment': 'Флаг проверки изображения'})
    urls: List["ImageUrl"] = Relationship(back_populates="image")

class Label(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={'comment': 'Идентификатор метки'})
    name: str = Field(sa_column_kwargs={'comment': 'Наименование метки'})

class ImageUrl(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"comment": "Идентификатор URL"}
    )
    image_id: int = Field(
        foreign_key="image.id",
        sa_column_kwargs={"comment": "Идентификатор изображения"}
    )
    url: str = Field(
        sa_column_kwargs={"comment": "URL изображения"}
    )

    # Обратная связь к таблице Image
    image: Image = Relationship(back_populates="urls")

    # Определяем внешнюю ссылку на главную таблицу Image
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['image.id']),
    )