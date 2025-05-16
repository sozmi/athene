
from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
from pathlib import Path

from db.repos.image_repository import select_image
from defenitions import ROOT_DIR
from auth import auth_handler
from tools import iter_file

image_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])

@image_router.get('/images/{id}', tags=['Images'])
def get_image_by_id(id: int):
    image = select_image(id)
    image_path = Path(f'{ROOT_DIR}/data/{image.path}')
    if not image_path.is_file():
        return {'error': 'Image not found on the server'}
    file = iter_file(image_path)
    return StreamingResponse(file)

@image_router.get('/temp/images/{path}', tags=['Images'])
def get_image_by_path(path: str):
    image_path = Path(f'{ROOT_DIR}/data/temp/images/{image.path}')
    if not image_path.is_file():
        return {'error': 'Image not found on the server'}
    file = iter_file(image_path)
    return StreamingResponse(file)