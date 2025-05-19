import pandas as pd
import streamlit as st

from scripts import check_access
from scripts.process.image import save_images_proc, load_unverify_images_proc, convert_json_to_arrays
from scripts.process.label import get_labels_proc, get_label_id_proc

check_access()
load_images = {}
if st.session_state.get('load_images_df'):
    load_images = st.session_state['load_images_df']
else:
    images = load_unverify_images_proc()
    load_images = convert_json_to_arrays(images)

data_df = pd.DataFrame(
    {
        "names": load_images['name'],
        "labels": load_images['label'],
        "images": load_images['url'],
    }
)
labels = get_labels_proc()
labels_name = [item['name'] for item in labels]

editor_df = st.data_editor(
    data_df,
    row_height=128,
    column_config={
        "images": st.column_config.ImageColumn(
            "Загруженные изображения", width="medium"
        ),
        "labels": st.column_config.SelectboxColumn("Выберите метку",
                                                   options=labels_name)
    },
    hide_index=True
)

if st.button("Подтвердить метки"):
    df_labels = editor_df['labels']
    edit_labels = []
    for label in df_labels:
        edit_labels.append(get_label_id_proc(label))

    res = save_images_proc(load_images['id'], edit_labels)
    st.write(res)
    if st.session_state.get('load_images_df'):
        st.session_state.pop('load_images_df')