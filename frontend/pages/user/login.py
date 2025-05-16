import streamlit as st
from st_pages import hide_pages
from scripts.process.user import log_proc

col1, col2 = st.columns(2)

with col1:
    usrnM = st.text_input('Логин', key=3, placeholder='uniquename')
    passW = st.text_input('Пароль', key=4, placeholder='pass123')

    if st.button('Войди!'):
        if not usrnM:
            st.error("Некорректный логин")
        if not passW:
            st.error("Некорректный пароль")
        else:
            log_proc(usrnM, passW)
            hide_pages(["Регистрация", "Вход"])
            st.stop()

with col2:
    st.image("https://static.streamlit.io/examples/dog.jpg")