from scripts import check_access, st
from scripts.process.label import get_labels_proc
from scripts.process.model import get_models_proc

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
    if not eps:
        st.error("Введите количество эпох!")
