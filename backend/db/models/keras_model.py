"""
Файл содержит описание моделей БД
"""
from typing import Optional
from sqlmodel import SQLModel, Field


class KerasModel(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={'comment': 'Идентификатор изображения'})
    path: str = Field(sa_column_kwargs={'comment': 'Наименование модели'})