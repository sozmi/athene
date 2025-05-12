"""
Запросы к БД
"""
from sqlmodel import Session, select
from backend.db.models.user_model import *
from backend.db import engine


def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement)
        return result.all()


def select_user(username):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        result = session.exec(statement)
        return result.first()