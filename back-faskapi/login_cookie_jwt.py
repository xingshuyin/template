import datetime
import hashlib
from pydantic import BaseModel
from typing import Optional, Annotated
from main import app
import jwt
from fastapi import Request, Response, Header, Cookie, HTTPException
import models_tortoise
from datetime import datetime as datetime_
from datetime import timedelta
from fastapi.responses import JSONResponse


SECRET_KEY = 'asddddddddddddddddddddd'
SINGLE_LOGIN = True
TOKEN_EXP = timedelta(hours=1)
REFRESH_EXP = timedelta(hours=2)
WHITE_API = ['/token/', '/token', '/create_user/', '/create_user']


class Login(BaseModel):
    username: str
    password: str
    captcha: str


@app.middleware("http")
async def refresh_token(request: Request, call_next):
    """
    刷新token / 验证token
    """
    response = await call_next(request)  # 执行真正的接口
    if request.url.path in WHITE_API:
        return response
    response, token_data, refresh_data = await parse_token(request, response)
    return response


async def parse_token(request: Request, response: Response):
    """
    解析token
    """
    token = request.cookies.get("token")
    refresh = request.cookies.get("refresh")
    token_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
    refresh_data = jwt.decode(refresh, SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
    if SINGLE_LOGIN:
        client = await get_client(request, token_data['user'])
        if token_data['client'] != client:
            return JSONResponse(status_code=401, content={'detail': '令牌无效'})
    time_now = datetime_.now().timestamp()
    if float(token_data['exp']) > time_now:
        return response
    elif float(token_data['exp']) < time_now and float(refresh_data['exp']) > time_now:
        token, refresh, token_data, refresh_data = await make_token(request, refresh_data['user'])
        response.set_cookie(key='token', value=token, httponly=True)
        response.set_cookie(key='refresh', value=refresh, httponly=True)
    else:
        return JSONResponse(status_code=401, content={'detail': '令牌过期'})
    return response, token_data, refresh_data


async def make_token(request: Request, user_id):
    """
    生成token
    """
    time_now = datetime_.now()
    client = await get_client(request, user_id)
    token_data = {
        'user': user_id,
        'exp': datetime_.timestamp(time_now + TOKEN_EXP),
        'iat': datetime_.timestamp(time_now),
        'client': client
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
    refresh_data = {
        'user': user_id,
        'exp': datetime_.timestamp(time_now + REFRESH_EXP),
        'iat': datetime_.timestamp(time_now),
        'client': client
    }
    refresh = jwt.encode(refresh_data, SECRET_KEY, algorithm='HS256')
    return token, refresh, token_data, refresh_data


async def encode_password(password: str):
    """
    加密密码
    """
    return hashlib.sha256(password.encode()).hexdigest()


async def get_client(request: Request, user_id=None) -> str:
    """
    获取客户端标识
    """
    return hashlib.md5((str(user_id) + request.client.host + request.headers.get('user-agent')).encode()).hexdigest()


@app.post("/token/", status_code=200)
async def token(request: Request, data: Login, response: Response):
    """
    登录/获取token
    """
    user_obj = await models_tortoise.user.all().filter(username=data.username)
    if len(user_obj) == 0:
        response.status_code = 401
        return {'detail': '账号或密码错误'}
    user_obj = user_obj[0]
    if (user_obj.password == await encode_password(data.password)):
        token, refresh, token_data, refresh_data = await make_token(request, user_obj.id)
        response.set_cookie(key='token', value=token, httponly=True)
        response.set_cookie(key='refresh', value=refresh, httponly=True)
        return {'detail': '登录成功'}
    else:
        response.status_code = 401
        return {'detail': '账号或密码错误'}


@app.post("/create_user/", status_code=201)
async def create_user(request: Request, data: Login, response: Response):
    if not await models_tortoise.user.exists(username=data.username):
        data.password = hashlib.sha256(data.password.encode()).hexdigest()
        u = await models_tortoise.user.create(username=data.username, password=data.password)
        await u.set_password(data.password)
        await models_tortoise.user_info.create(user_id=u.id)
        return {'detail': '注册成功'}
    else:
        response.status_code = 401
        return {'detail': '用户名已存在'}
