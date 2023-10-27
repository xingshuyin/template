from tortoise import fields, models as models_tortoise
from tool import pydantic_model_creator
from typing import Any
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List
from starlette.exceptions import HTTPException
from typing import TypeVar
from fastapi import Request
from tortoise.queryset import (
    BulkCreateQuery,
    BulkUpdateQuery,
    ExistsQuery,
    Q,
    F,
    QuerySet,
    QuerySetSingle,
    RawSQLQuery,
)
from starlette.datastructures import URL, Address, FormData, Headers, QueryParams, State


class Status(BaseModel):
    detail: str


class Model(models_tortoise.Model):
    id = fields.IntField(pk=True)
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间', null=True)
    update_time = fields.DatetimeField(auto_now=True, description='更新时间', null=True)
    dept_belong = fields.IntField(description='所属部门id', null=True)
    creator = fields.IntField(description='创建人id', null=True)
    # public_model = False  # 是否公开, 公开数据list查询不受部门限制, 但受角色的接口

    @classmethod
    def pydantic(cls):
        if not hasattr(cls, "_pydantic_model"):
            cls._pydantic_model = pydantic_model_creator(cls, name=cls.Meta.table)
        return cls._pydantic_model

    class Meta:
        abstract = True

    @classmethod
    def init_router(cls, app: FastAPI):
        cls.pydantic()

        @app.get("/" + cls.Meta.table, status_code=200)
        async def list(request: Request, response: Response):
            return await cls.list_obj(request, response)

        @app.post("/" + cls.Meta.table, response_model=cls.pydantic(), status_code=200)
        async def create(request: Request, response: Response, obj: cls.pydantic()):
            return await cls.create_obj(request, response, obj)

        @app.get("/" + cls.Meta.table + "/{id}", response_model=cls.pydantic(), status_code=200)
        async def get(request: Request, response: Response, id: int):
            return cls.get_obj(request, response, id)

        @app.put("/" + cls.Meta.table + "/{id}", response_model=user.pydantic(), status_code=200)
        async def update(request: Request, response: Response, id: int, obj: cls.pydantic()):
            return await cls.update_obj(request, response, id, obj)

        @app.delete("/" + cls.Meta.table + "/{id}", status_code=200)
        async def delete(request: Request, response: Response, id: int):
            return await cls.delete_obj(request, response, id)

    @classmethod
    async def list_obj(cls, request: Request, response: Response):
        q = request.query_params._dict
        if q.get("page") and q.get("limit"):
            page = int(q.get("page"))
            limit = int(q.get("limit"))
            queryset = cls.all()
            for i in ['page', 'limit', 'values[]', 'defer[]', 'extra[]']:
                if i in q.keys():
                    del q[i]
            queryset, q = await cls.filter(request, queryset, q)
            return await cls.pydantic().from_queryset(queryset.offset((page - 1) * limit).limit(limit))
        else:
            response.status_code = 400
            return {'detal': 'no page or limit'}

    @classmethod
    async def get_obj(cls, request: Request, response: Response, id: int):
        return await cls.pydantic().from_queryset_single(cls.get(id=id))

    @classmethod
    async def create_obj(cls, request: Request, response: Response, obj):

        obj_ = await cls.create(**obj.model_dump(exclude_unset=True))
        return await cls.pydantic().from_tortoise_orm(obj_)

    @classmethod
    async def update_obj(cls, request: Request, response: Response, id: int, obj):
        await cls.filter(id=id).update(**obj.model_dump(exclude_unset=True))
        return await cls.pydantic().from_queryset_single(cls.get(id=id))

    @classmethod
    async def delete_obj(cls, request: Request, response: Response, id: int):
        deleted_count = await cls.filter(id=id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {id} not found")
        return Status(detail=f"Deleted user {id}")

    @classmethod
    async def special_filter(queryset: QuerySet, query: dict):

        return queryset

    @classmethod
    async def filter(cls, request: Request, queryset: QuerySet, query: QueryParams):
        fields = queryset.model._meta.fields
        print(fields)
        if 'extra[]' in request.path_params.keys():  # TODO:获取额外字段
            extra = request.path_params.getlist('extra[]')
            for i in extra:
                queryset = queryset.annotate(**{i: F(i)})
                fields.append(i)
        if 'values[]' in request.path_params.keys():  # TODO:选择字段
            values = request.GET.getlist('values[]')
            for i in values[:]:
                if i not in fields:
                    values.remove(i)
            fields = values
        if 'defer[]' in request.path_params.keys():  # TODO:排除字段
            for i in request.GET.getlist('defer[]'):
                if i in fields:
                    fields.remove(i)
        queryset = queryset.filter(**query)
        return (queryset, query)


class user(Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=128, null=True)
    role = fields.JSONField(default=[])
    dept = fields.IntField(null=True)
    is_super = fields.BooleanField(default=False)

    @classmethod
    async def create_obj(cls, request: Request, obj):
        return {'detail': 'can create user faild'}

    class PydanticMeta:
        exclude = ["password"]

    class Meta:
        table = "user"
        table_description = '用户'


class user_info(Model):
    icon = fields.CharField(max_length=200, null=True)
    birthday = fields.DateField(max_length=200, null=True)
    signature = fields.CharField(max_length=200, null=True)
    user = fields.ForeignKeyField('models.user', related_name='user_info', null=True)
    name = fields.CharField(max_length=200, null=True)
    gender = fields.CharField(max_length=200, null=True)
    email = fields.CharField(max_length=100, null=True)
    phone = fields.CharField(max_length=12, null=True)
    follow_user = fields.ManyToManyField('models.user', related_name='follow_user', null=True)
    article_like = fields.ManyToManyField('models.article', related_name='article_like', null=True)
    article_collect = fields.ManyToManyField('models.article', related_name='article_collect', null=True)

    class Meta:
        table = "user_info"
        table_description = '用户信息'


class interface(Model):
    name = fields.CharField(max_length=20, unique=True)
    key = fields.CharField(max_length=20, unique=True)
    method = fields.CharField(max_length=10, default="GET")
    path = fields.CharField(max_length=100, default="/")
    model = fields.CharField(max_length=100)
    modelname = fields.CharField(max_length=100)

    class Meta:
        table = "interface"
        table_description = '接口'


class role(Model):
    name = fields.CharField(max_length=20, unique=True)
    key = fields.CharField(max_length=20, unique=True)
    permission = fields.IntField(default=0)
    interface = fields.ManyToManyField('models.interface')

    class Meta:
        table = "role"
        table_description = '角色'


class dept(Model):
    name = fields.CharField(max_length=20, unique=True)
    key = fields.CharField(max_length=20, unique=True)
    parent = fields.ForeignKeyField('models.dept', null=True, related_name='children')
    owner = fields.CharField(max_length=20, null=True)

    class Meta:
        table = "dept"
        table_description = '部门'


class menu(Model):
    name = fields.CharField(max_length=20, unique=True)
    label = fields.CharField(max_length=20, unique=True)
    component = fields.CharField(max_length=128, unique=True)
    parent = fields.ForeignKeyField('models.menu', null=True, related_name='children')
    path = fields.CharField(max_length=100, null=True)
    icon = fields.CharField(max_length=20, null=True)
    sort = fields.IntField(default=0)
    is_link = fields.BooleanField(default=False)
    is_catalog = fields.BooleanField(default=False)
    disable = fields.BooleanField(default=False)

    class Meta:
        table = "menu"
        table_description = '菜单'


class area(Model):
    name = fields.CharField(max_length=100, null=True)
    code = fields.CharField(max_length=20, null=True)
    level = fields.IntField(max_length=10, null=True)
    lat = fields.CharField(max_length=10, null=True)
    lng = fields.CharField(max_length=10, null=True)
    parent = fields.ForeignKeyField('models.area', null=True, related_name='children')

    class Meta:
        table = "area"
        table_description = '地区'


class log(Model):
    username = fields.CharField(max_length=50, null=True)
    ip = fields.CharField(max_length=50, null=True)
    agent = fields.CharField(max_length=50, null=True)
    browser = fields.CharField(max_length=200, null=True)
    os = fields.CharField(max_length=200, null=True)
    continent = fields.CharField(max_length=50, null=True)
    country = fields.CharField(max_length=50, null=True)
    province = fields.CharField(max_length=50, null=True)
    city = fields.CharField(max_length=50, null=True)
    district = fields.CharField(max_length=50, null=True)
    isp = fields.CharField(max_length=50, null=True)
    area_code = fields.CharField(max_length=50, null=True)
    country_english = fields.CharField(max_length=50, null=True)
    country_code = fields.CharField(max_length=50, null=True)
    longitude = fields.CharField(max_length=50, null=True)
    latitude = fields.CharField(max_length=50, null=True)

    class Meta:
        table = "log"
        table_description = '日志'


class article(Model):
    name = fields.CharField(max_length=200, null=True)
    user = fields.ForeignKeyField('models.user', null=True)
    source = fields.CharField(max_length=200, null=True)
    source_root = fields.CharField(max_length=200, null=True)
    source_sub = fields.CharField(max_length=200, null=True)
    tag = fields.JSONField(default=[])
    content = fields.TextField(null=True)
    file = fields.JSONField(max_length=200, null=True)
    image = fields.JSONField(max_length=200, null=True)
    video = fields.JSONField(max_length=200, null=True)
    url = fields.CharField(max_length=200, null=True)
    url_hash = fields.CharField(max_length=200, null=True)
    type = fields.IntField(default=0, null=True)
    view = fields.IntField(default=0, null=True)
    like = fields.IntField(default=0, null=True)
    comment = fields.IntField(default=0, null=True)
    collect = fields.IntField(default=0, null=True)
    is_delete = fields.BooleanField(default=0, null=True)
    is_top = fields.BooleanField(default=0, null=True)
    is_hot = fields.BooleanField(default=0, null=True)
    is_original = fields.BooleanField(default=0, null=True)
    is_recommend = fields.BooleanField(default=0, null=True)

    class Meta:
        table = "article"
        table_description = '文章'


class article_comment(Model):
    user = fields.ForeignKeyField('models.user', null=True)
    article = fields.ForeignKeyField('models.article', null=True)
    content = fields.TextField(null=True)
    reply = fields.ForeignKeyField('models.article_comment', related_name='replyed', null=True)
    root = fields.ForeignKeyField('models.article_comment', related_name='rooted', null=True)

    class Meta:
        table = 'article_comment'
        table_description = '文章评论'
