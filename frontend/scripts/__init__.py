import streamlit as st

def check_access():
    access_token = st.session_state.get("access_token")
    if not access_token:
        st.error("Для доступа к данной странице войдите или зарегистрируйтесь")
        st.stop()
    return access_token

def get_access_header():
    access_token = check_access()
    return {"Authorization": f"Bearer {access_token}"}