import requests
from scripts import st, get_access_header
from scripts.process import API_LOAD_IMAGES, API_GET_UNVERIFY_IMAGES, API_GET_TEMP_IMAGE, API_APPROVE_IMAGES
from scripts.process.label import get_label_name_proc


def load_images_proc(label, count, query):
    """
    Получение списка меток, включая идентификаторы
    :param label:
    :param count:
    :param query:
    :return: наименования скаченных файлов
    """
    payload = {
        "label_name": label,
        "count": count,
        "query": query
    }
    response = requests.post(API_LOAD_IMAGES, params=payload, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["images"]

def load_unverify_images_proc():
    """
    Получение списка меток, включая идентификаторы
    :return: наименования скаченных файлов
    """
    response = requests.get(API_GET_UNVERIFY_IMAGES, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["images"]

def save_images_proc(ids, labels):
    param = {"ids": ids, "lids": labels}
    response = requests.post(API_APPROVE_IMAGES, json=param, headers=get_access_header())
    if response.status_code != 200:
        st.error(response.text)
        st.stop()
    return response.json()["detail"]

def convert_json_to_arrays(images):
    names, urls, labels, ids = [[], [], [], []]
    for image in images:
        names.append(image['path'])
        urls.append(f'{API_GET_TEMP_IMAGE}{image["path"]}')
        labels.append(get_label_name_proc(image['lid']))
        ids.append(image['id'])
    return {'id': ids, "name": names, "url": urls, "label": labels}