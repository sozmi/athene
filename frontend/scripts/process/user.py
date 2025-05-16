import requests
import streamlit as st

from scripts import get_access_header
from scripts.process import API_LOGIN, HEADER_ONLY_JSON, API_REGISTER, API_ACCOUNT


def log_proc(login, password):
    payload = {
        "username": login,
        "password": password
    }
    response = requests.post(API_LOGIN, json=payload, headers=HEADER_ONLY_JSON)
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    # Отобразить ответ в приложении Streamlit
    st.session_state["access_token"] = response.json()['token']


def reg_proc(login, pass1, pass2, email):
    payload = {
        "username": login,
        "password": pass1,
        "password2": pass2,
        "email": email
    }
    response = requests.post(API_REGISTER, json=payload, headers=HEADER_ONLY_JSON)
    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    st.session_state["access_token"] = response.json()['token']

def info_proc():
    response = requests.get(API_ACCOUNT, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    return response.json()
