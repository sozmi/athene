import jwt
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta

from starlette.status import HTTP_401_UNAUTHORIZED

from backend.db.repos.user_repository import select_user

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'supersecret'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=8),
            'iat': datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Срок действия токена закончился')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Неверный токен')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)):
        credentials_exception = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Ошибка авторизации')
        uid = self.decode_token(auth.credentials)
        if uid is None:
            raise credentials_exception
        uid = int(uid)
        user = select_user(uid)
        if user is None:
            raise credentials_exception
        return user

auth_handler = AuthHandler()