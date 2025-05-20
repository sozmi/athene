FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN --mount=type=cache,target=/root/.cache \
    pip install -r /code/requirements.txt

COPY ./ /code/app

ENV PYTHONPATH /code/app/

#CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]