from scripts import check_access, st
from scripts.process.model import get_models_proc, get_model_history_proc, get_model_info_proc
import plotly.express as px

check_access()
models = get_models_proc()
index = None
if st.session_state.get('model'):
    index = models.index(st.session_state['model'])
model = st.selectbox("Выберите модель", models, index=index,
                     placeholder="Выберите модель...")
st.session_state['model'] = model

if model:
    col1, col2 = st.columns(2)
    with col1:
        df = get_model_history_proc(model)

        fig_acc = px.line(df, x='epoch', y=['accuracy', 'val_accuracy'], title="Точность модели по эпохам")
        fig_acc.update_xaxes(title_text='Эпоха')
        fig_acc.update_yaxes(title_text='Точность')
        st.plotly_chart(fig_acc)

        fig_loss = px.line(df, x='epoch', y=['loss', 'val_loss'], title="Потери модели по эпохам")
        fig_loss.update_xaxes(title_text='Эпоха')
        fig_loss.update_yaxes(title_text='Потери')
        st.plotly_chart(fig_loss)
    with col2:
        st.code(get_model_info_proc(model))