"""
Файл содержит запросы на сервер, относящиеся к Labels - api
"""
import requests
import streamlit as st

from scripts import get_access_header
from scripts.process import API_GET_LABELS


def get_labels_proc():
    """
    Получение списка меток, включая идентификаторы
    :return: json объектов меток
    """
    response = requests.get(API_GET_LABELS, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["labels"]

