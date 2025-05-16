import streamlit as st

from scripts import check_access
from scripts.process.model import get_models_proc, classification_proc

check_access()
col1, col2 = st.columns(2)
with col1:
    css = '''
    <style>
    [data-testid="stFileUploaderDropzone"] div div::before {content:"Перетащите и отпустите изображение"}
    [data-testid="stFileUploaderDropzone"] div div span{display:none;}
    [data-testid="stFileUploaderDropzone"] div div::after {font-size: .8em; 
    content:"Максимальный размер каждого файла 200MB"}
    [data-testid="stFileUploaderDropzone"] div div small{display:none;}
    [data-testid='stFileUploaderDropzone'] > [data-testid='stBaseButton-secondary'] {
        margin-top: 4px;
        margin-bottom: -1px;
        text-indent: -9999px;
        line-height: 0;

        &::after {
            line-height: initial;
            content: "Выбрать файл";
            text-indent: 0;
        }
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
    uploaded_file = st.file_uploader('Выберите изображение', type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file)
        st.session_state['image'] = uploaded_file
    else:
        st.session_state['image'] = None

with col2:
    model = st.selectbox(
        "Выберите модель для классификации",
        (get_models_proc()),
        index=None,
        placeholder="Выберите модель...")
    st.session_state['model'] = model
    if st.button('Классифицировать'):
        state = st.session_state
        model = state.get('model')
        image = state.get('image')
        if not model:
            st.error('Выберите модель для классификации')
        elif not image:
            st.error('Выберите изображение')
        else:
            result = classification_proc(image, model)
            st.write(result)
