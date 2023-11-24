# from tomlkit import datetime
import copy
import datetime
import time
from itertools import chain
from pathlib import Path

import pandas as pd
from django.db import models
from django.db.models import F, QuerySet
from django.contrib.auth.models import AnonymousUser
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.query import BaseIterable
from django.utils import timezone
from rest_framework import exceptions, filters, status
from rest_framework.decorators import action
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from ..authentication import MyJWTAuthentication

from ..utils import ratelimit
from ..models import *
from ..permission import SuperPermisssion
from ..utils import get_time


# 模型序列化(附加外键序列化)
def to_dict(instance, deep=2):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        v = f.value_from_object(instance)
        if isinstance(f, ManyToManyField):  # 外键序列化,使用它必须继承本模型
            if deep > 0:
                v = [i.model_to_dict(deep=deep - 1) for i in v] if v else []
            else:
                v = [i.id for i in v] if v else []
        elif isinstance(f, ForeignKey):  # 外键序列化,使用它必须继承本模型
            if deep > 0:
                v = f.related_model.objects.get(pk=v).model_to_dict(
                    deep=deep - 1) if v else None
            else:
                pass
        if isinstance(f, DateTimeField):
            v = v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        data[f.name] = v

    return data


def get_all_sub_dept(dept_id):
    r = [dept_id]
    childern = dept.objects.filter(parent__id=dept_id)
    if len(childern):
        for i in childern:
            r.extend(get_all_sub_dept(i.id))
    return r


def get_depts(request, instance):
    user_dept_id = getattr(request.user, "dept_id", None)
    if not user_dept_id:  # 用户没有部门, 就不受部门限制
        return True
    if not getattr(instance, "dept_belong", None):  # 数据没有部门, 就不受部门限制
        return True
    if instance.dept_belong == None:  # 数据没有部门, 就不受部门限制
        return True
    if not hasattr(request.user, "role"):
        return [user_dept_id]

    # 3. 根据所有角色 获取所有权限范围
    # (0, "仅本人数据权限"),
    # (1, "本部门及以下数据权限"),
    # (2, "本部门数据权限"),
    # (3, "全部数据权限"),
    # (4, "自定数据权限")
    role_list = request.user.role
    permission_list = []  # 权限范围列表
    for role in role_list:
        # 判断用户是否为超级管理员角色/如果拥有[全部数据权限]则返回所有数据
        role = role.objects.get(id=role)
        if 3 == role.permission or role.is_admin == True:
            return True
        permission_list.append(role.permission)
    permission_list = list(set(permission_list))
    # 4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
    if 0 in permission_list:
        return []

    # 5. 自定数据权限 获取部门，根据部门过滤
    dept_list = []
    for p in permission_list:
        if p == 4:
            for i in request.user.role:
                dept_list.extend(role.objects.get(
                    id=i).dept.values_list("dept__id", flat=True))
        elif p == 2:
            dept_list.append(user_dept_id)
        elif p == 1:
            dept_list.extend(get_all_sub_dept(user_dept_id))
    return dept_list


def deal_permission(request, queryset):
    """
    判断是否为超级管理员:
    """
    if (queryset.model.public_model):
        return queryset

    if type(request.user) == AnonymousUser:  # 匿名用户不受部门限制,但受特定的角色的接口限制
        return queryset
    if not getattr(request.user, 'is_super', None):
        # 0. 获取用户的部门id，没有部门则返回空
        user_dept_id = getattr(request.user, "dept_id", None)
        if not user_dept_id:
            return queryset.none()

        # 1. 判断过滤的数据是否有创建人所在部门 "dept_belong" 字段
        if not getattr(queryset.model, "dept_belong", None):
            return queryset

        # 2. 如果用户没有关联角色则返回本部门数据
        if not hasattr(request.user, "role"):
            return queryset.filter(dept_belong=user_dept_id)

        # 3. 根据所有角色 获取所有权限范围
        # (0, "仅本人数据权限"),
        # (1, "本部门及以下数据权限"),
        # (2, "本部门数据权限"),
        # (3, "全部数据权限"),
        # (4, "自定数据权限")
        role_list = request.user.role
        permission_list = []  # 权限范围列表
        for role in role_list:
            # 判断用户是否为超级管理员角色/如果拥有[全部数据权限]则返回所有数据
            role = role.objects.get(id=role)
            if 3 == role.permission or role.is_admin == True:
                return queryset
            permission_list.append(role.permission)
        permission_list = list(set(permission_list))
        # 4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
        if 0 in permission_list:
            return queryset.filter(creator=request.user.id, dept_belong=user_dept_id)

        # 5. 自定数据权限 获取部门，根据部门过滤
        dept_list = []
        for p in permission_list:
            if p == 4:
                for i in request.user.role:
                    dept_list.extend(role.objects.get(
                        id=i).dept.values_list("dept__id", flat=True))
            elif p == 2:
                dept_list.append(user_dept_id)
            elif p == 1:
                dept_list.extend(get_all_sub_dept(user_dept_id))
        if queryset.model._meta.model_name == 'dept':
            return queryset.filter(id__in=list(set(dept_list)))
        return queryset.filter(dept_belong__in=list(set(dept_list)))
    else:
        return queryset


# 处理特殊搜索参数
def special_filter(request: HttpRequest, queryset: QuerySet, filter_dict):
    fields = [i.name for i in queryset.model._meta.fields]
    model_name = queryset.model._meta.model_name
    or_filter = None
    filter_dict_ = copy.deepcopy(filter_dict)
    for i in filter_dict_.keys():
        if '__in' in i:  # 列表包含查询
            filter_dict[i.strip('[]')] = request.GET.getlist(i)
            print(filter_dict)
            del filter_dict[i]
        if 'or[' in i:  # 多条件或者
            value = request.GET.get(i)
            key = i.replace('or[', '').replace(']', '')
            if or_filter != None:
                or_filter = or_filter | Q(**{key: value})
            else:
                or_filter = Q(**{key: value})
            del filter_dict[i]
    if or_filter != None:
        queryset = queryset.filter(or_filter)
    if 'sort' in filter_dict.keys():
        queryset = queryset.order_by(*request.GET.getlist('sort'))
        del filter_dict['sort']
    if 'order' in filter_dict.keys():
        queryset = queryset.order_by(*request.GET.getlist('order'))
        del filter_dict['order']
    # if 'parent_name' in filter_dict.keys():
    #     queryset = queryset.filter(parent__name=filter_dict['parent_name'])
    #     del filter_dict['parent_name']
    # if 'create_start' in filter_dict.keys():
    #     queryset = queryset.filter(
    #         create_time__gte=filter_dict['create_start'])
    #     del filter_dict['create_start']
    # if 'create_end' in filter_dict.keys():
    #     queryset = queryset.filter(create_time__lte=filter_dict['create_end'])
    #     del filter_dict['create_end']

    # for i in ['name', 'project', 'city', 'county', 'legal_person', 'leader', 'industry']:  # 所有字符串包含类型的过滤
    #     if i in filter_dict.keys():
    #         queryset = queryset.filter(**{i + '__contains': filter_dict[i]})
    #         del filter_dict[i]
    return queryset, filter_dict


def get_extra_value(request, queryset):
    fields = [i.name for i in queryset.model._meta.fields]
    # queryset.model  TODO:获取queryset的model对象
    model_name = queryset.model._meta.model_name
    if 'parent' in fields:
        queryset = queryset.annotate(parent_name=F("parent__name"))
        fields.append('parent_name')
    if 'area' in fields:
        queryset = queryset.annotate(area_name=F("area__name"))
        fields.append('area_name')
    if 'dept' in fields:
        queryset = queryset.annotate(dept_name=F("dept__name"))
        fields.append('dept_name')
    if model_name in ['menu']:
        queryset = queryset.annotate(parent_label=F("parent__label"))
        fields.append('parent_label')
    if 'extra[]' in request.GET.dict():  # TODO:获取额外字段
        extra = request.GET.getlist('extra[]')
        for i in extra:
            queryset = queryset.annotate(**{i: F(i)})
            fields.append(i)
    if model_name in ['user']:
        if not getattr(request.user, 'is_super', None):
            raise exceptions.AuthenticationFailed(
                '用户不存在',
                "no_active_account",
            )
    return queryset, fields


def prefetch_related(queryset: QuerySet):
    if queryset.model._meta.model_name in ['backenduser']:
        queryset = queryset.prefetch_related('role')
    return queryset


# 通用list方法
# @get_time
@ratelimit(key='ip', rate='3/s')
def list_common(self, request: HttpRequest, *args):
    # jwt = MyJWTAuthentication()
    # user = jwt.authenticate(request)[0] # 手动验证用户, 用于 authentication_classes=[] 的接口

    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    filter_dict = request.GET.dict()
    temp_dict = request.GET.dict()
    queryset: QuerySet = self.get_queryset()
    queryset = deal_permission(request, queryset)
    if (page and limit):
        for k, v in temp_dict.items():
            if v == '' or v == 'null' or v == 'undefined':  # 删除无用过滤字段
                del filter_dict[k]
        for i in ['page', 'limit', 'values[]', 'defer[]', 'extra[]']:
            if i in filter_dict.keys():
                del filter_dict[i]
        queryset, filter_dict = special_filter(request, queryset, filter_dict)
        queryset = queryset.filter(**filter_dict)
        queryset, fields = get_extra_value(request, queryset)

        if 'values[]' in temp_dict.keys():  # TODO:选择字段
            values = request.GET.getlist('values[]')
            for i in values[:]:
                if i not in fields:
                    values.remove(i)
            fields = values
        if 'defer[]' in temp_dict.keys():  # TODO:排除字段
            for i in request.GET.getlist('defer[]'):
                if i in fields:
                    fields.remove(i)
        # print(queryset.query) # TODO:查看查询语句
        r = queryset.values(*fields)

        total = r.count()
        r = r[(page - 1) * limit:page * limit]
        if r is not None:
            return Response({'data': list(r), 'page': page, 'limit': limit, 'total': total}, 200)
    return Response({'detail': '未分页'}, 400)


# 获取单个对象方法
def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    r = serializer.data
    for i in instance._meta.fields:
        if isinstance(i, models.fields.DateTimeField):
            # if type(i) == models.fields.DateTimeField:
            if v := instance.__dict__[i.name]:
                r[i.name] = deal_value(v)
    return Response(r)


# 创建方法
def create(self, request, *args, **kwargs):
    dept_belong = getattr(request.user, 'dept_belong', None)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    user_id = getattr(user, 'id', None)
    model_name = serializer.Meta.model.__name__

    fields = serializer.fields.keys()
    if 'dept_belong' in fields:
        serializer.validated_data['dept_belong'] = dept_belong
    if 'creator' in fields:
        serializer.validated_data['creator'] = user_id

    instance = serializer.save()
    if instance._meta.object_name == 'user':
        instance.set_password(instance.password)
        instance.save()
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=201, headers=headers)


# 更新方法
def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    depts = get_depts(request, instance)
    if getattr(request.user, 'is_super', None) or depts == True or instance.dept_belong in depts:
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        return Response({'detail': '没有修改权限'}, 400)


# 删除方法
def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    depts = get_depts(request, instance)
    if getattr(request.user, 'is_super', None) or depts == True or instance.dept_belong in depts:
        self.perform_destroy(instance)
        return Response({'detail': '删除成功'}, 200)
    else:
        return Response({'detail': '没有删除权限'}, 400)


# 多项更新
@action(['PUT'], url_path='mult_update', url_name='多项更新', detail=False)
def mult_update(self, request: HttpRequest, *args, **kwargs):
    id_list = request.GET.getlist('id[]')
    querys = request.POST.dict()
    queryset: QuerySet = self.get_queryset()
    queryset = queryset.filter(id__in=id_list)
    r = queryset.update(**querys)  # TODO:queryset 批量更新
    return Response({'msg': '批量修改成功成功', 'data': r}, 200)


# TODO:数据导出
@action(['POST'], url_path='export', url_name='数据导出', detail=False)
def export(self, request: HttpRequest, *args, **kwargs):
    filter_dict = request.data
    temp_dict = request.data
    columns = [i for i in request.data.get('columns') if i['show']]
    for k, v in temp_dict.items():
        if v == '':
            del filter_dict[k]
    for i in ['page', 'limit', 'columns']:
        if i in filter_dict.keys():
            del filter_dict[i]
    queryset: QuerySet = self.get_queryset()
    queryset = deal_permission(request, queryset)
    queryset, filter_dict = special_filter(request, queryset, filter_dict)
    queryset = queryset.filter(**filter_dict)
    queryset, fields = get_extra_value(request, queryset)
    r = queryset.values_list(*[i['prop'] for i in columns])
    d = pd.DataFrame(list(r), columns=[i['label'] for i in columns])
    p = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/")
    filename = queryset.model._meta.model_name + str(int(time.time() * 1000))
    if not os.path.exists(f'{p}/media/export/'):
        os.makedirs(f'{p}/media/export/')
    d.to_excel(f'{p}/media/export/{filename}.xlsx')
    return Response({'url': f'media/export/{filename}.xlsx'}, status=200)


# 字段处理
def deal_value(v):
    if type(v) == datetime.datetime:  # TODO:request- 处理时间
        # v = timezone.localtime(v)  # 获取时区为当前时区的时间; 时间=时间值+时区
        return timezone.datetime.strftime(v, "%Y-%m-%d %H:%M:%S")  # 获取时间的时间值
    return v


class MyValuesIterable(BaseIterable):
    """
    Iterable returned by QuerySet.values() that yields a dict for each row.
    """

    def __iter__(self):
        queryset = self.queryset
        query = queryset.query
        compiler = query.get_compiler(queryset.db)

        # extra(select=...) cols are always at the start of the row.
        names = [
            *query.extra_select,
            *query.values_select,
            *query.annotation_select,
        ]
        # TODO:request-QuerySet修改values  去掉_id
        names = [i.rstrip('_id') if i.endswith("_id") else i for i in names]
        indexes = range(len(names))
        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size):
            # TODO:request-QuerySet修改values  去掉_id
            yield {names[i]: deal_value(row[i]) for i in indexes}


# 自定义queryset
class MyQuerySet(QuerySet):

    def values(self, *fields, **expressions):  # TODO:QuerySet-values实现
        fields += tuple(expressions)
        clone = self._values(*fields, **expressions)
        clone._iterable_class = MyValuesIterable
        return clone

    def clone(self, queryset):
        self.model = queryset.model
        self._db = queryset._db
        self._hints = queryset._hints
        self._query = queryset._query
        self._result_cache = queryset._result_cache
        self._sticky_filter = queryset._sticky_filter
        self._for_write = queryset._for_write
        self._prefetch_related_lookups = queryset._prefetch_related_lookups
        self._prefetch_done = queryset._prefetch_done
        self._known_related_objects = queryset._known_related_objects
        self._iterable_class = queryset._iterable_class
        self._fields = queryset._fields
        self._defer_next_filter = queryset._defer_next_filter
        self._deferred_filter = queryset._deferred_filter


# 序列化器生成器
def model_serializer(m, inherit, *args, **kwargs):

    class Meta:
        model = m
        fields = "__all__"
        read_only_fields = ['id']

    ser = type(m._meta.label + "_ser", inherit, {'Meta': Meta})
    return ser


# 模型视图生成器
def model_viewset(m, inherit_viewset, inherit_serializer, **kwargs):
    viewset = type(
        m._meta.label + "_view",
        inherit_viewset,
        dict(
            {
                'queryset': MyQuerySet(m),
                'serializer_class': model_serializer(m, inherit_serializer),
                'filter_backends': [filters.SearchFilter],
                # 'permission_classes': [],  //权限管理器
                # 'authentication_classes': [],  // 认证管理器
                'mult_update': mult_update,
                'export': export,
                'list': list_common,
                'destroy': destroy,
                'update': update,
                'create': create,
                'retrieve': retrieve,
            },
            **kwargs))
    return viewset


# 生成所有视图及链接的基础
view_list = [
    {
        "url": "dept",  # restful链接基础url
        "label": "部门",
        # 对应视图集
        "viewset": model_viewset(dept, (ModelViewSet, ), (ModelSerializer, ), model_name="部门")
    },
    {
        "url": "file",
        "label": "文件",
        "viewset": model_viewset(file, (ModelViewSet, ), (ModelSerializer, ), model_name="文件")
    },
    {
        "url": "menu",
        "label": "菜单",
        "viewset": model_viewset(menu, (ModelViewSet, ), (ModelSerializer, ), model_name="菜单")
    },
    {
        "url": "role",
        "label": "角色",
        "viewset": model_viewset(role, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[SuperPermisssion], model_name="角色")
    },
    {
        "url": "user",
        "label": "用户",
        "viewset": model_viewset(user, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[SuperPermisssion], model_name="用户")
    },
    {
        "url": "log",
        "label": "日志",
        "viewset": model_viewset(log, (ModelViewSet, ), (ModelSerializer, ), model_name="日志")
    },
    {
        "url": "area",
        "label": "区域",
        "viewset": model_viewset(area, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[], model_name="区域")
    },
    {
        "url": "interface",
        "label": "接口",
        "viewset": model_viewset(interface, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[SuperPermisssion], model_name="接口")
    },
    {
        "url": "enterprise",
        "label": "企业",
        "viewset": model_viewset(enterprise, (ModelViewSet, ), (ModelSerializer, ), model_name="企业")
    },
    {
        "url": "article",
        "label": "文章",
        "viewset": model_viewset(article, (ModelViewSet, ), (ModelSerializer, ), model_name="文章")
    },
    {
        "url": "spider",
        "label": "爬虫",
        "viewset": model_viewset(spider, (ModelViewSet, ), (ModelSerializer, ), model_name="爬虫")
    },
]
