import os
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
from pathlib import Path

import tools
from db import session
from db.models.image_model import Image
from db.repos.image_repository import select_image, select_label_by_name, create_label, select_all_non_verify_images
from defenitions import ROOT_DIR
from auth import auth_handler
from net.parser import Parser
from net.proxy import ProxyManager
from net.validator import Validator
from tools import iter_file

image_router = APIRouter()
pm = ProxyManager()
p = Parser(pm)
@image_router.get('/images/{id}', tags=['Images'], dependencies=[Depends(auth_handler.auth_wrapper)])
def get_image_by_id(id: int):
    image = select_image(id)
    if image.lid is None:
        image_path = Path(f'{ROOT_DIR}/data/images/dump/{image.path}')
    else:
        image_path = Path(f'{ROOT_DIR}/data/images/{image.lid}/{image.path}')
    if not image_path.is_file():
        return {'error': 'Изображение не найдено на сервере!'}
    file = iter_file(image_path)
    return StreamingResponse(file)

@image_router.get('/temp/images/{path}', tags=['Images'])
def get_image_by_path(path: str):
    image_path = Path(f'{ROOT_DIR}/data/temp/images/{path}')
    if not image_path.is_file():
        return {'error': 'Изображение не найдено на сервере!'}
    file = iter_file(image_path)
    return StreamingResponse(file)

@image_router.post('/images/image/load', tags=['Images'], dependencies=[Depends(auth_handler.auth_wrapper)])
def load_images(query: str, label_name: str, count: int):
    label = select_label_by_name(label_name)
    if not label:
        label = create_label(label_name)
        tools.mkdir(f'{ROOT_DIR}/data/images/{label.id}')
    dirs = [Path(f'{ROOT_DIR}/data/temp/images'), Path(f'{ROOT_DIR}/data/images/{label.id}')]
    valid = Validator(dirs, (512, 512))
    p.set_validator(valid)
    p.download_images(query, label.id, count)
    images = select_all_non_verify_images()
    return {"images": images}

@image_router.get('/images/image/unverify', tags=['Images'], dependencies=[Depends(auth_handler.auth_wrapper)])
def get_unverify_images():
    images = select_all_non_verify_images()
    return {"images": images}

@image_router.post('/images/approve', tags=['Images'], dependencies=[Depends(auth_handler.auth_wrapper)])
def approve_images(ids: List[int], lids: List[int]):
    for iid, lid in zip(ids, lids):
        session.begin()
        image = session.query(Image).get(iid)
        old_path = f'{ROOT_DIR}/data/temp/images/{image.path}'
        pref_path = f'{ROOT_DIR}/data/images'
        if lid is None:
            os.replace(old_path, f'{pref_path}/dump/{image.path}')
        else:
            os.replace(old_path, f'{pref_path}/{lid}/{image.path}')
        image.lid = lid
        image.verify = True
        session.commit()
    return {"detail": "Подтверждено!"}