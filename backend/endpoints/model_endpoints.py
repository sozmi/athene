from http.client import HTTPException

from fastapi import APIRouter, Depends, UploadFile, File
from starlette.responses import StreamingResponse
from pathlib import Path

from backend.neuro.model import ModelManager
from backend.db.repos.keras_repository import select_model, select_all_models
from defenitions import ROOT_DIR
from backend.auth import auth_handler
from backend.tools import iter_file
mm = ModelManager()
model_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])

@model_router.get('/models/{id}', tags=['Models'])
def get_model(id: int):
    image = select_model(id)
    image_path = Path(f'{ROOT_DIR}/data/models/{image.path}')
    if not image_path.is_file():
        return {'error': 'Модель не найдена на сервере'}
    file = iter_file(image_path)
    return StreamingResponse(file)

@model_router.get('/models', tags=['Models'])
def get_models():
    models = select_all_models()
    models_name = []
    for m in models:
        model_path = Path(f'{ROOT_DIR}/data/models/{m.path}')
        if model_path.is_file():
            models_name.append(m.path)
    return models_name

@model_router.post('/classify', tags=['Models'])
def classify(model_path: str, image: UploadFile = File(...)):
    try:
        contents = image.file.read()
        image_path = ROOT_DIR + "/data/temp/" + image.filename
        with open(image_path, 'wb') as f:
            f.write(contents)
        return mm.classify(image_path, ROOT_DIR + "/data/models/" + model_path)
    except Exception:
        raise HTTPException(status_code=500, detail='Слишком долгое ожидание')
    finally:
        image.file.close()

