from fastapi import APIRouter, Depends

from backend.db.repos.image_repository import select_all_labels, select_label
from backend.auth import auth_handler

label_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])

@label_router.get('/labels', tags=['Labels'])
def get_labels():
    labels = select_all_labels()
    return {'labels': labels}

@label_router.get('/labels/{id}', tags=['Labels'])
def get_label(id: int):
    labels = select_label(id)
    return {'labels': labels}
