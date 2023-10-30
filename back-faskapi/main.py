# pylint: disable=E0611,E0401

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import login_cookie_jwt
import models_tortoise
from tortoise.models import ModelMeta

app = FastAPI(title="Tortoise ORM FastAPI example")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for k, v in models_tortoise.__dict__.items():  # 注册所有路由
    if (type(v) == ModelMeta):
        if k != 'Model':
            v.init_router(app)

register_tortoise(
    app,
    # db_url="sqlite://tortoise.sql",
    # modules={"models": ["models_tortoise"]},
    generate_schemas=True,
    add_exception_handlers=True,
    config={
        'db_url': "sqlite://tortoise.sql",
        'connections': {
            'default': "sqlite://tortoise.sql",
        },
        'apps': {
            'models': {
                'models': ['models_tortoise'],
                'default_connection': 'default',
            }
        },
        'use_tz': True,
        'timezone': 'Asia/Shanghai',
    }
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
