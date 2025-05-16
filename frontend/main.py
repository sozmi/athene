import streamlit as st
from st_pages import add_page_title, get_nav_from_toml, hide_pages

st.set_page_config(layout="wide")

nav = get_nav_from_toml("pages/pages_sections.toml")

pg = st.navigation(nav)
add_page_title(pg)
access_token = st.session_state.get("access_token")
if not access_token:
    hide_pages(["Выход", "Информация", "Модели", "Изображения"])
else:
    hide_pages(["Регистрация", "Вход"])
pg.run()