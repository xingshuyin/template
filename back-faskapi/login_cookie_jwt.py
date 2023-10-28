import datetime
import hashlib
from pydantic import BaseModel
from typing import Optional, Annotated
from main import app
import jwt
from fastapi import Request, Response, Header, Cookie, HTTPException
SECRET_KEY = 'asddddddddddddddddddddd'
from models_tortoise import user
from datetime import datetime as datetime_
from datetime import timedelta
from fastapi.responses import JSONResponse


single_login = True


class Login(BaseModel):
    username: str
    password: str
    captcha: str


@app.middleware("http")
async def refresh_token(request: Request, call_next):
    """
    刷新token
    """
    response = await call_next(request)
    if request.url.path == '/token/':
        return response
    response = await parse_token(request, response)
    return response


async def parse_token(request: Request, response: Response):
    """
    解析token
    """
    token = request.cookies.get("token")
    refresh = request.cookies.get("refresh")
    token_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
    refresh_data = jwt.decode(refresh, SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
    if single_login:
        client = await get_client(request, token_data['user'])
        if token_data['client'] != client:
            return JSONResponse(status_code=401, content={'detail': '令牌无效'})
    time_now = datetime_.now().timestamp()
    if float(token_data['exp']) > time_now:
        return response
    elif float(token_data['exp']) < time_now and float(refresh_data['exp']) > time_now:
        token, refresh = await make_token(request, refresh_data['user'])
        response.set_cookie(key='token', value=token, httponly=True)
        response.set_cookie(key='refresh', value=refresh, httponly=True)
    else:
        return JSONResponse(status_code=401, content={'detail': '令牌过期'})
    return response


async def make_token(request: Request, user_id):
    """
    生成token
    """
    time_now = datetime_.now()
    client = await get_client(request, user_id)
    token = jwt.encode({
        'user': user_id,
        'exp': datetime_.timestamp(time_now + timedelta(seconds=5)),
        'iat': datetime_.timestamp(time_now),
        'client': client
    }, SECRET_KEY, algorithm='HS256')
    refresh = jwt.encode({
        'user': user_id,
        'exp': datetime_.timestamp(time_now + timedelta(seconds=10)),
        'iat': datetime_.timestamp(time_now),
        'client': client
    }, SECRET_KEY, algorithm='HS256')
    return token, refresh


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
    user_obj = await user.all().filter(username=data.username)
    if len(user_obj) == 0:
        response.status_code = 401
        return {'detail': '账号或密码错误'}
    user_obj = user_obj[0]
    if (user_obj.password == await encode_password(data.password)):
        token, refresh = await make_token(request, user_obj.id)
        response.set_cookie(key='token', value=token, httponly=True)
        response.set_cookie(key='refresh', value=refresh, httponly=True)
        return {'detail': '登录成功'}
    else:
        response.status_code = 401
        return {'detail': '账号或密码错误'}


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
