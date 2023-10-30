from tortoise import fields, models as models_tortoise
from tool import pydantic_model_creator
import copy
from fastapi import FastAPI, Response
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from typing import TypeVar
from fastapi import Request
from tortoise.queryset import (
    F,
    QuerySet,
)
import login_cookie_jwt
from tortoise.contrib.pydantic.base import PydanticModel


class Status(BaseModel):
    detail: str


from tortoise import fields
from datetime import datetime


class DatetimeField(fields.DatetimeField):
    # 重写to_db_value方法，将Python的datetime对象转换为字符串
    def to_db_value(self, value: datetime, instance) -> str:
        # 使用strftime方法来格式化时间字符串
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (self.auto_now_add and getattr(instance, self.model_field_name) is None)
        ):
            value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            setattr(instance, self.model_field_name, value)
        return value
    # 重写to_python_value方法，将字符串转换为Python的datetime对象

    def to_python_value(self, value: str) -> datetime:
        return value


class Model(models_tortoise.Model):
    id = fields.IntField(pk=True)
    create_time = DatetimeField(auto_now_add=True, description='创建时间', null=True)
    update_time = DatetimeField(auto_now=True, description='更新时间', null=True)
    dept_belong = fields.IntField(description='所属部门id', null=True)
    creator = fields.IntField(description='创建人id', null=True)
    # public_model = False  # 是否公开, 公开数据list查询不受部门限制, 但受角色的接口

    @classmethod
    def pydantic(cls) -> PydanticModel:
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
        q = copy.deepcopy(request.query_params._dict)
        if q.get("page") and q.get("limit"):
            page = int(q.get("page"))
            limit = int(q.get("limit"))
            queryset = cls.all()
            model = queryset.model
            for i in ['page', 'limit', 'values[]', 'defer[]', 'extra[]', 'order', 'sort']:
                if i in q.keys():
                    del q[i]
            queryset, q, fields = await cls.filter_fields(request, queryset, q)
            queryset = queryset.offset((page - 1) * limit).limit(limit)
            queryset = await queryset.prefetch_related(*model._meta.m2m_fields)
            r = []
            for i in queryset:
                item = {}
                for j in model._meta.m2m_fields:  # many to many
                    item.update({j: [o.pk for o in await getattr(i, j,[])]})
                for j in model._meta.o2o_fields:  # one to one
                    print(await getattr(i, j))
                    item.update({j: (await getattr(i, j)).pk})
                for j in model._meta.backward_fk_fields:  # many to one
                    item.update({j: [o.pk for o in await getattr(i, j,[])]})
                for j in fields:
                    item.update({j: getattr(i, j)})
                r.append(item)
            # queryset = await queryset.values(*fields)
            # print(queryset)
            # queryset = await cls.pydantic().from_queryset(queryset)
            return r
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
    async def filter_fields(cls, request: Request, queryset: QuerySet, query: dict):
        fields = queryset.model._meta.db_native_fields + \
            queryset.model._meta.db_default_fields + queryset.model._meta.db_complex_fields
        fields = [i[0] for i in fields]
        if 'extra[]' in request.query_params.keys():  # TODO:获取额外字段
            extra = request.query_params.getlist('extra[]')
            for i in extra:
                queryset = queryset.annotate(**{i: F(i)})
                fields.append(i)
        if 'values[]' in request.query_params.keys():  # TODO:选择字段
            values = request.query_params.getlist('values[]')
            for i in values:
                if i not in fields:
                    values.remove(i)
            fields = values
        if 'defer[]' in request.query_params.keys():  # TODO:排除字段
            for i in request.query_params.getlist('defer[]'):
                if i in fields:
                    fields.remove(i)
        if hasattr(queryset.model, 'PydanticMeta'):
            if hasattr(queryset.model.PydanticMeta, 'exclude'):
                for i in queryset.model.PydanticMeta.exclude:
                    fields.remove(i)
        if 'order' in request.query_params.keys():
            order = request.query_params.getlist('order')
            queryset = queryset.order_by(*order)
        if 'sort' in request.query_params.keys():
            order = request.query_params.getlist('sort')
            queryset = queryset.order_by(*order)
        queryset = queryset.filter(**query)
        return queryset, query, fields


class user(Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=128, null=True)
    role = fields.JSONField(default=[])
    dept = fields.IntField(null=True)
    is_super = fields.BooleanField(default=False)

    @classmethod
    async def create_obj(cls, request: Request, obj):
        return {'detail': 'create user faild'}

    class PydanticMeta:
        exclude = ["password"]

    class Meta:
        table = "user"
        table_description = '用户'

    async def set_password(self, password):
        self.password = await login_cookie_jwt.encode_password(password)
        await self.save()

    async def check_password(self, password):
        p = await login_cookie_jwt.encode_password(password)
        return p == self.password


class user_info(Model):
    icon = fields.CharField(max_length=200, null=True)
    birthday = fields.DateField(max_length=200, null=True)
    signature = fields.CharField(max_length=200, null=True)
    user = fields.OneToOneField('models.user', related_name='user_info', null=True)
    name = fields.CharField(max_length=200, null=True)
    gender = fields.CharField(max_length=200, null=True)
    email = fields.CharField(max_length=100, null=True)
    phone = fields.CharField(max_length=12, null=True)
    follow_user = fields.ManyToManyField('models.user_info', related_name='followed_user', db_constraint=False, null=True)
    article_like = fields.ManyToManyField('models.article', related_name='article_liked', null=True)
    article_collect = fields.ManyToManyField('models.article', related_name='article_collected', null=True)

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
    interface = fields.ManyToManyField('models.interface', related_name='role', null=True)

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
