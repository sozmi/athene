import streamlit.web.bootstrap
def start():
    streamlit.web.bootstrap.run("web/frontend/sections.py", False, [], [])
