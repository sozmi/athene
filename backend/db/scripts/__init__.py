"""
В этом файле происходит создание и заполнение БД
"""
from sqlmodel import SQLModel

from db import engine, session
import db.models.image_model
import db.models.keras_model
import db.models.user_model

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
