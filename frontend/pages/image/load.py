import pandas as pd
import streamlit as st
from streamlit import button
from scripts.process.label import get_labels_proc
from scripts.process.image import load_images_proc, save_images_proc
from scripts import check_access
check_access()

labels = get_labels_proc()
label = st.selectbox("Выберите метку", labels, index=None,
                     placeholder="Выберите метку...")
query = st.text_input('Запрос', key=1, placeholder='полярный медведь')
count = st.text_input('Количество изображений', key=2, placeholder='100')
if not button("Загрузить"):
    st.stop()

if not query:
    st.error("Введите запрос для поиска картинок!")
    st.stop()
if not count:
    st.error("Введите количество изображений!")
    st.stop()
if not label:
    st.error("Выберите метку к которой будут относиться изображения!")
    st.stop()

info_list = load_images_proc(label, count, query)
data_df = pd.DataFrame(
    {
        "names": info_list['names'],
        "images": info_list['urls'],
        "labels": info_list['labels'],
    }
)

editor_df = st.data_editor(
    data_df,
    column_config={
        "images": st.column_config.ImageColumn(
            "Загруженные изображения", width="medium"
        ),
        "labels": st.column_config.SelectboxColumn("Выберите метку", options=labels)
    },
    hide_index=True
)

if st.button("Подтвердить метки"):
    edit_labels = editor_df['labels'].to_string(index=False)
    names = data_df['names'].to_string(index=False)
    save_images_proc(names, edit_labels)