import datetime
import hashlib
from pydantic import BaseModel
from typing import Optional, Annotated
from main import app
import jwt
from fastapi import Request, Response, Header, Cookie
SECRET_KEY = 'asddddddddddddddddddddd'
from models_tortoise import user
from datetime import datetime as datetime_
from datetime import timedelta
from starlette.exceptions import HTTPException


class Login(BaseModel):
    username: str
    password: str
    captcha: str


async def parse_token(token: str):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='令牌过期')
    return token_data


async def encode_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


@app.post("/token/", status_code=200)
async def token(request: Request, data: Login, response: Response):
    user_obj = await user.all().filter(username=data.username)
    if len(user_obj) == 0:
        response.status_code = 401
        return {'detail': '账号或密码错误'}
    user_obj = user_obj[0]
    if (user_obj.password == await encode_password(data.password)):
        time_now = datetime_.now()
        token = jwt.encode({
            'user': user_obj.id,
            'exp': datetime_.timestamp(time_now + timedelta(seconds=5)),
            'iat': datetime_.timestamp(time_now),
            'is_super': user_obj.is_super,
        }, SECRET_KEY, algorithm='HS256')
        refresh = jwt.encode({
            'user': user_obj.id,
            'exp': datetime_.timestamp(time_now + timedelta(seconds=5)),
            'iat': datetime_.timestamp(time_now),
            'is_super': user_obj.is_super,
        }, SECRET_KEY, algorithm='HS256')
        response.set_cookie(key='token', value=token, httponly=True)
        response.set_cookie(key='refresh', value=refresh, httponly=True)
        return {'token': token, 'refresh': refresh}
    else:
        response.status_code = 401
        return {'detail': '账号或密码错误'}


@app.post("/refresh/", status_code=200)
async def refresh(request: Request, response: Response, refresh: Annotated[str | None, Cookie()] = None):
    """
    Generate token for user
    """
    token_data = await parse_token(refresh)
    time_now = datetime_.now()
    token = jwt.encode({
        'user': token_data['user'],
        'exp': datetime_.timestamp(time_now + timedelta(seconds=5)),
        'iat': datetime_.timestamp(time_now),
        'is_super': token_data['is_super'],
    }, SECRET_KEY, algorithm='HS256')
    response.set_cookie(key="token", value=token, httponly=True)
    return token


@app.post("/create_user/", status_code=201)
async def create_user(request: Request, data: Login, response: Response):
    print(user.exists(username=data.username))
    if not await user.exists(username=data.username):
        data.password = hashlib.sha256(data.password.encode()).hexdigest()
        await user.create(username=data.username, password=data.password)
        return {'detail': '注册成功'}
    else:
        response.status_code = 401
        return {'detail': '用户名已存在'}
