from st_pages import hide_pages

from scripts import check_access
import streamlit as st

check_access()
st.write("Вы действительно хотите выйти?")
if st.button('Да'):
    st.session_state.clear()
    hide_pages(["Выход", "Модели", "Изображения"])
if st.button('Нет'):
    st.switch_page('pages/home.py')
