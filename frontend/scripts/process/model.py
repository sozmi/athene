import http.client

import requests
import streamlit as st
from altair import param

from scripts.process import API_MODELS, API_MODEL_HISTORY, API_MODEL_INFO, API_CLASSIFY, API_TRAIN
from scripts import get_access_header


def get_models_proc():
    response = requests.get(API_MODELS, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["models"]


def get_model_history_proc(model_path):
    param = {"path": model_path}
    response = requests.get(API_MODEL_HISTORY, params=param, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["data"]


def get_model_info_proc(model_path):
    param = {"path": model_path}
    response = requests.get(API_MODEL_INFO, params=param, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["data"]


def classification_proc(image, model):
    payload = {"model_path": model}
    files = {"image": image.getvalue()}
    response = requests.post(API_CLASSIFY, params=payload, files=files, headers=get_access_header())
    http.client.HTTPConnection.debuglevel = 1
    if response.status_code != 200:
        st.error(response.text)
        #st.stop()
        return None
    return response.json()

def train_proc(model_path, lids, epc):
    params = {'model_filename': model_path, 'epc': epc, 'lids': lids}
    data = {"lids": lids}
    response = requests.post(API_TRAIN, params=params, json=lids, headers=get_access_header())
    http.client.HTTPConnection.debuglevel = 1
    if response.status_code != 200:
        st.error(response.text)
        #st.stop()
        return None
    return response.json()