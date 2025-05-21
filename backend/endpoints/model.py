import os
from http.client import HTTPException
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File
from pathlib import Path

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from neuro.model import ModelManager
from db.repos.keras_repository import select_model_by_id, select_all_models, select_model_by_id, select_model_by_path
from defenitions import ROOT_DIR
from auth import auth_handler

mm = ModelManager()
model_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])

@model_router.get('/models/{id}', tags=['Models'])
def get_model(id: int):
    model = select_model_by_id(id)
    model_path = Path(f'{ROOT_DIR}/data/models/{model.path}')
    if not model_path.is_file():
        return {'error': 'Модель не найдена на сервере'}
    return model.path

@model_router.get('/models', tags=['Models'])
def get_models():
    models = select_all_models()
    models_name = []
    for m in models:
        model_path = Path(f'{ROOT_DIR}/data/models/{m.path}')
        if model_path.is_file():
            models_name.append(m.path)
    return {"models": models_name}

@model_router.post('/classify', tags=['Models'])
def classify(model_path: str, image: UploadFile = File(...)):
    try:
        contents = image.file.read()
        image_path = ROOT_DIR + "/data/temp/" + image.filename
        with open(image_path, 'wb') as f:
            f.write(contents)
        res = mm.classify(image_path, ROOT_DIR + "/data/models/" + model_path, model_path)
        os.remove(image_path)
        return res
    except Exception:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Слишком долгое ожидание')
    finally:
        image.file.close()

@model_router.get('/model/info', tags=['Models'])
def get_model_info(path: str):
    model_path = ROOT_DIR + "/data/models/" + path
    mm.load_model(model_path)
    summary_str = []
    mm.model.summary(print_fn=lambda x: summary_str.append(x))
    summary_str = "\n".join(summary_str)
    return {"data": summary_str}


@model_router.get("/model/history", tags=['Models'])
def get_model_history(path: str):
    model = select_model_by_path(path)
    history_path = ROOT_DIR + "/data/models/history/" + model.history_path
    df = pd.read_csv(history_path, sep=',', engine='python')
    result = df.to_dict(orient="records")
    return {"data": result}

@model_router.post('/train', tags=['Models'])
def train(model_filename: str, epc: int, lids: List[int]):
    model = select_model_by_path(model_filename)
    lids.sort()
    classes = [str(n) for n in lids]
    model_name = model_filename.removesuffix('.keras')
    if model:
        mm.load_model(f'{ROOT_DIR}/data/models/{model_filename}')
        mm.train(model_name, classes, epc)
    else:
        mm.train_new(model_name, classes, epc)
    return {"detail": "Модель обучена"}