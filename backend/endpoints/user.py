from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from db import session
from db.models.user_model import UserInput, User, UserLogin
from db.repos.user_repository import select_all_users, select_user_by_name
from auth import auth_handler

user_router = APIRouter()

@user_router.post('/registration', status_code=HTTP_201_CREATED, tags=['Users'],
                  description='Регистрация нового пользователя')
def register(user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Пользователь с таким именем уже зарегистрирован')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hashed_pwd, email=user.email)
    session.add(u)
    session.commit()
    token = auth_handler.encode_token(u.id)
    return {'token': token}

@user_router.post('/login', tags=['Users'])
def login(user: UserLogin):
    user_found = select_user_by_name(user.username)
    print(user_found)
    if not user_found:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Пользователь не существует')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Неверный пароль')
    token = auth_handler.encode_token(user_found.id)
    return {'token': token}


@user_router.get('/account', tags=['Users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user
