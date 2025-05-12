"""
Запросы к БД
"""
from sqlmodel import Session, select
from backend.db.models.keras_model import *
from backend.db import engine


def select_all_models():
    with Session(engine) as session:
        statement = select(KerasModel)
        result = session.exec(statement)
        result = result.all()
        return result


def select_model(id):
    with Session(engine) as session:
        statement = select(KerasModel).where(KerasModel.id == id)
        result = session.exec(statement)
        return result.first()

