from scripts import check_access, st
from scripts.process.label import get_labels_proc, get_label_id_proc
from scripts.process.model import get_models_proc, train_proc

check_access()
models = get_models_proc()
index = None
if st.session_state.get('model'):
    index = models.index(st.session_state['model'])
model = st.selectbox("Выберите модель", models, index=index,
                     accept_new_options=True,
                     placeholder="Выберите модель...")


st.subheader("Параметры")
eps = st.text_input('Эпохи', key=1, placeholder='5')
options = get_labels_proc()
labels_name = [item['name'] for item in options]
selection = st.pills("Использовать метки", labels_name, selection_mode="multi")
if st.button('Обучить модель'):
    if not model:
        st.error("Укажите модель")
        st.stop()
    if not eps:
        st.error("Введите количество эпох!")
        st.stop()
    if not selection:
        st.error("Выберите метки!")
        st.stop()
    edit_labels = []
    for label in selection:
        edit_labels.append(get_label_id_proc(label))
    res = train_proc(model, edit_labels, eps)
    st.write(res)
