import streamlit as st
from st_pages import hide_pages

from scripts.process.user import reg_proc

col1, col2 = st.columns(2)
with col1:
    username = st.text_input('Логин', key=1, placeholder='uniquename')
    pass1 = st.text_input('Пароль', key=2, placeholder='pass123')
    pass2 = st.text_input('Повторите пароль', placeholder='pass123')
    email = st.text_input('Почта', placeholder='example@mail.ru')
    if st.button('Зарегистрируй меня!'):
        if not username:
            st.write("Некорректный логин")
        elif not pass1 or not pass2:
            st.write("Некорректный пароль")
        elif pass1!=pass2:
            st.write("Пароли не совпадают")
        elif not email:
            st.write("Некорректная почта")
        else:
            reg_proc(username, pass1, pass2, email)
            hide_pages(["Регистрация", "Вход"])
            st.stop()

with col2:
    st.image("https://static.streamlit.io/examples/cat.jpg")
