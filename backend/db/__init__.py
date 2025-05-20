"""
Объявления глобальных констант, относящихся к БД
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url_db = 'postgresql+psycopg2://user:100@postgres:5432/athene_db'
engine = create_engine(url_db, echo=True, isolation_level="READ COMMITTED")
session = Session(bind=engine)