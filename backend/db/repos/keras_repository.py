"""
Запросы к БД
"""
from sqlmodel import Session, select
from db.models.keras_model import *
from db import engine


def select_all_models():
    with Session(engine) as session:
        statement = select(KerasModel)
        result = session.exec(statement)
        result = result.all()
        return result


def select_model_by_id(id):
    with Session(engine) as session:
        statement = select(KerasModel).where(KerasModel.id == id)
        result = session.exec(statement)
        return result.first()

def select_model_by_path(path):
    with Session(engine) as session:
        statement = select(KerasModel).where(KerasModel.path == path)
        result = session.exec(statement)
        return result.first()

