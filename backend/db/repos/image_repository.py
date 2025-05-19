"""
Запросы к БД
"""
from sqlmodel import Session, select
from db.models.image_model import *
from db import engine, session


def select_all_images():
    with Session(engine) as session:
        statement = select(Image)
        result = session.exec(statement)
        return result.all()

def select_all_non_verify_images():
    with Session(engine) as session:
        statement = select(Image).where(Image.verify == False)
        result = session.exec(statement)
        return result.all()


def select_image(id):
    with Session(engine) as session:
        statement = select(Image).where(Image.id == id)
        result = session.exec(statement)
        return result.first()

def select_all_url():
    urls = []
    with Session(engine) as session:
        statement = select(Image.urls)
        result = session.exec(statement)
        image_urls = result.all()
        for row in image_urls:
            urls += row
        return urls


def select_image_by_path(filename, is_verify):
    with Session(engine) as session:
        statement = select(Image).where(Image.path == filename and Image.verify == is_verify)
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

def select_label_by_name(name):
    with Session(engine) as session:
        statement = select(Label).where(Label.name == name)
        result = session.exec(statement)
        return result.first()

def add_url_to_image(filename, is_verify, url):
    with Session(engine) as session:
        image = select_image_by_path(filename, is_verify)
        image.urls.append(url)
        session.commit()

def create_label(name):
    label = Label(name=name)
    session.add(label)
    session.commit()
    return label

def create_image(label, path, url, verify=False):
    image = Image(lid=label, path=path, url=url, verify=False)
    session.add(image)
    session.commit()