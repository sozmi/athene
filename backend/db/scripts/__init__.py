"""
В этом файле происходит создание и заполнение БД
"""
from sqlmodel import Session

from backend.db.models.keras_model import *

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    #create_db()

def create_image(label):
    image = Image(lid=label, path='test')
    return image

def create_label(name):
    label = Label(name=name)
    return label

def create_db():
    polar = create_label('полярный медведь')
    brown = create_label('бурый медведь')

    with Session(engine) as session:
        session.add(polar)
        session.add(brown)
        session.commit()
        session.add(create_image(polar.id))
        session.add(create_image(polar.id))
        session.add(create_image(brown.id))
        session.commit()