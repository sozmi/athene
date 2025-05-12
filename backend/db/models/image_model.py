"""
Файл содержит описание моделей БД
"""
from typing import Optional
from sqlmodel import SQLModel, Field


class Image(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={'comment': 'Идентификатор изображения'})
    lid: int = Field(foreign_key='label.id', sa_column_kwargs={'comment': 'Идентификатор метки'})
    path: str = Field(sa_column_kwargs={'comment': 'Относительный путь к изображению'})

class Label(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={'comment': 'Идентификатор метки'})
    name: str = Field(sa_column_kwargs={'comment': 'Наименование метки'})