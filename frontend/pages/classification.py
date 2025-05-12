import streamlit as st
from backend import get_models

def pic_process(image_path):
    #res1 = model.evaluate()
    #st.text_input(res1)

def click_class():



col1, col2 = st.columns(2)
with col1:
    folder_path = st.text_input('Path .jpg')

with col2:
    st.button('Classify', on_click=click_class)

    option = st.selectbox(
        "Выберите модель для классификации",
        (get_models()),
        index=None,
        placeholder="Выберите модель...")