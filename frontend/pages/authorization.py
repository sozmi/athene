import streamlit as st
from backend import UserInput, UserLogin
from backend import register, login

def reg_proc(val1, val2, val3):
    usr = UserInput(username=val1, password=val2, email=val3)
    mess = register(usr)
    st.write(mess)

def log_proc(val1, val2):
    us2 = UserLogin(username=val1, password=val2)
    mess = login(us2)
    st.write(mess)


col1, col2 = st.columns(2)
with col1:
    st.title("Регистрация")
    usrnm = st.text_input('Логин', key=1, placeholder='uniquename')
    pass1 = st.text_input('Пароль', key=2, placeholder='pass123')
    pass2 = st.text_input('Повторите пароль', placeholder='pass123')
    email = st.text_input('Почта', placeholder='example@mail.ru')
    if st.button('Зарегистрируй меня!'):
        if not usrnm:
            st.write("Некорректный логин")
        elif not pass1 or not pass2:
            st.write("Некорректный пароль")
        elif pass1!=pass2:
            st.write("Пароли не совпадают")
        elif not email:
            st.write("Некорректная почта")
        else:
            reg_proc(usrnm, pass1, email)

with col2:
    st.title("Вход")
    usrnM = st.text_input('Логин', key=3, placeholder='uniquename')
    passW = st.text_input('Пароль', key=4, placeholder='pass123')

    if st.button('Войди!'):
        if not usrnM:
            st.write("Некорректный логин")
        if not passW:
            st.write("Некорректный пароль")
        else:
            log_proc(usrnM, passW)

if 'stop' not in st.session_state:
    st.session_state['stop'] = False

if st.button('Остановить приложение'):
    st.session_state['stop'] = True

if st.session_state['stop']:
    st.stop()
