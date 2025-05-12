
from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
from pathlib import Path

from backend.db.repos.image_repository import select_image
from defenitions import ROOT_DIR
from backend.auth import auth_handler
from backend.tools import iter_file

image_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])

@image_router.get('/images/{id}', tags=['Images'], dependencies=[Depends(auth_handler.get_current_user)])
def get_image_id(id: int):
    image = select_image(id)
    image_path = Path(f'{ROOT_DIR}/data/{image.path}')
    if not image_path.is_file():
        return {'error': 'Image not found on the server'}
    file = iter_file(image_path)
    return StreamingResponse(file)