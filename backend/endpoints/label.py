from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND

from db.repos.image_repository import select_all_labels, select_label, select_label_by_name
from auth import auth_handler

label_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])

@label_router.get('/labels', tags=['Labels'])
def get_labels():
    labels = select_all_labels()
    return {'labels': labels}

@label_router.get('/label', tags=['Labels'])
def get_label(id: Optional[int] = None, name: Optional[str] = None):
    if id:
        label = select_label(id)
    elif name:
        label = select_label_by_name(name)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Не указан ни один из параметров!')
    if label is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Метка не найдена на сервере!')
    return {'label': label}