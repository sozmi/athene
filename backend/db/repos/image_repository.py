"""
Запросы к БД
"""
from sqlmodel import Session, select
from backend.db import engine


def select_all_images():
    with Session(engine) as session:
        statement = select(Image)
        result = session.exec(statement)
        return result.all()


def select_image(id):
    with Session(engine) as session:
        statement = select(Image).where(Image.id == id)
        result = session.exec(statement)
        return result.first()


def select_all_labels():
    with Session(engine) as session:
        statement = select(Label)
        result = session.exec(statement)
        return result.all()


def select_label(id):
    with Session(engine) as session:
        statement = select(Label).where(Label.id == id)
        result = session.exec(statement)
        return result.first()

