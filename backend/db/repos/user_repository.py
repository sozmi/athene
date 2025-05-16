"""
Запросы к БД
"""
from sqlmodel import Session, select
from db.models.user_model import *
from db import engine


def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement)
        return result.all()


def select_user_by_name(username):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        result = session.exec(statement)
        return result.first()

def select_user_by_id(id):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        result = session.exec(statement)
        return result.first()