import streamlit as st
from streamlit import button

from scripts.process import API_GET_TEMP_IMAGE
from scripts.process.label import get_labels_proc, get_label_name_proc
from scripts.process.image import load_images_proc, convert_json_to_arrays
from scripts import check_access
check_access()

labels = get_labels_proc()
labels_name = [item['name'] for item in labels]
label = st.selectbox("Выберите метку", labels_name, index=None,
                     accept_new_options=True,
                     placeholder="Выберите метку...")
query = st.text_input('Запрос', key=1, placeholder='полярный медведь')
count = st.text_input('Количество изображений', key=2, placeholder='100')

if button("Загрузить"):
    if not query:
        st.error("Введите запрос для поиска картинок!")
        st.stop()
    if not count:
        st.error("Введите количество изображений!")
        st.stop()
    if not label:
        st.error("Выберите метку к которой будут относиться изображения!")
        st.stop()
    images = load_images_proc(label, count, query)
    st.session_state['load_images_df'] = convert_json_to_arrays(images)
    st.switch_page('pages/image/approve.py')