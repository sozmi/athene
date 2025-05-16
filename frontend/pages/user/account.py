import streamlit as st
from scripts.process.user import info_proc

info = info_proc()
st.write(f"**Идентификатор:** {info['id']}")
st.write(f"**Логин:** {info['username']}")
st.write(f"**Почта:** {info['email']}")
st.write(f"**Создан:** {info['created_at']}")
st.markdown("---")