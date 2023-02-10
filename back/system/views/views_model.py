'''
Filename     : views_model.py
Author       : xingshuyin xingshuyin@outlook.com
Date         : 2022-10-31 19:40:52
LastEditors  : xingshuyin xingshuyin@outlook.com
LastEditTime : 2022-11-30 12:55:43
FilePath     : \wjt\back\system\views\views_model.py
Description  : 微镜头所有模型的restful规范接口

Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
'''
from django.db import models
from django.utils import timezone
from django.forms import model_to_dict
from django.db.models import QuerySet
from django.db.models import F
from django.db.models.query import BaseIterable
from django.views.decorators.cache import cache_page
from django.db.models.fields.related import ManyToManyField, ForeignKey
from rest_framework import filters, serializers, status, exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework.request import Request, HttpRequest
from rest_framework.response import Response
from pathlib import Path
from itertools import chain
from tomlkit import datetime
from ..models import *
from ..utils import get_time
from ..permission import SuperPermisssion
import json
import time
import pandas as pd


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
    print(opts.fields)
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
                v = f.related_model.objects.get(pk=v).model_to_dict(deep=deep - 1) if v else None
            else:
                pass
        if isinstance(f, DateTimeField):
            v = v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        data[f.name] = v

    return data


# 处理特殊搜索参数
def deal_special_params(request: HttpRequest, queryset: QuerySet, filter_dict):
    fields = [i.name for i in queryset.model._meta.fields]
    model_name = queryset.model._meta.model_name

    if 'sort' in filter_dict.keys():
        queryset = queryset.order_by(filter_dict['sort'])
        del filter_dict['sort']
    if 'parent_name' in filter_dict.keys():
        queryset = queryset.filter(parent__name=filter_dict['parent_name'])
        del filter_dict['parent_name']
    if 'create_start' in filter_dict.keys():
        queryset = queryset.filter(createAt__gte=filter_dict['create_start'])
        del filter_dict['create_start']
    if 'create_end' in filter_dict.keys():
        queryset = queryset.filter(createAt__lte=filter_dict['create_end'])
        del filter_dict['create_end']

    for i in ['name', 'project', 'city', 'county', 'legal_person', 'leader', 'industry']:  # 所有字符串包含类型的过滤
        if i in filter_dict.keys():
            queryset = queryset.filter(**{i + '__contains': filter_dict[i]})
            del filter_dict[i]
    return queryset, filter_dict


def get_all_sub_dept(dept_id):
    r = [dept_id]
    childern = Dept.objects.filter(parent__id=dept_id)
    if len(childern):
        for i in childern:
            r.extend(get_all_sub_dept(i.id))
    return r


def deal_permission(request, queryset):
    """
    判断是否为超级管理员:
    """
    if not request.user.is_super:
        # 0. 获取用户的部门id，没有部门则返回空
        user_dept_id = getattr(request.user, "dept_id", None)
        if not user_dept_id:
            return queryset.none()

        # 1. 判断过滤的数据是否有创建人所在部门 "dept_belong_id" 字段
        if not getattr(queryset.model, "dept_belong_id", None):
            return queryset

        # 2. 如果用户没有关联角色则返回本部门数据
        if not hasattr(request.user, "role"):
            return queryset.filter(dept_belong_id=user_dept_id)

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
            role = Role.objects.get(id=role)
            if 3 == role.permission or role.is_admin == True:
                return queryset
            permission_list.append(role.permission)
        permission_list = list(set(permission_list))
        # 4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
        if 0 in permission_list:
            return queryset.filter(creator_id=request.user.id, dept_belong_id=user_dept_id)

        # 5. 自定数据权限 获取部门，根据部门过滤
        dept_list = []
        for p in permission_list:
            if p == 4:
                for i in request.user.role:
                    dept_list.extend(Role.objects.get(id=i).dept.values_list("dept__id", flat=True))
            elif p == 2:
                dept_list.append(user_dept_id)
            elif p == 1:
                dept_list.extend(get_all_sub_dept(user_dept_id))
        if queryset.model._meta.model_name == 'dept':
            return queryset.filter(id__in=list(set(dept_list)))
        return queryset.filter(dept_belong_id__in=list(set(dept_list)))
    else:
        return queryset


def get_extra_value(request, queryset):
    fields = [i.name for i in queryset.model._meta.fields]
    model_name = queryset.model._meta.model_name  # queryset.model  TODO:获取queryset的model对象
    if 'parent' in fields:
        queryset = queryset.annotate(parent_name=F("parent__name"))
    if 'area' in fields:
        queryset = queryset.annotate(area_name=F("area__name"))
    if 'dept' in fields:
        queryset = queryset.annotate(dept_name=F("dept__name"))
    if model_name in ['menuinterface']:
        queryset = queryset.annotate(menu_name=F('menu__name'), menu_label=F('menu__label'))
    if model_name in ['user']:
        if not request.user.is_super:
            raise exceptions.AuthenticationFailed(
                '用户不存在',
                "no_active_account",
            )
    return queryset


def prefetch_related(queryset: QuerySet):
    if queryset.model._meta.model_name in ['backenduser']:
        queryset = queryset.prefetch_related('role')
    return queryset


# 通用list方法
@get_time
def list_common(self, request: HttpRequest, *args):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    filter_dict = request.GET.dict()
    temp_dict = request.GET.dict()
    queryset: QuerySet = self.get_queryset()
    queryset = deal_permission(request, queryset)
    if (page and limit):
        for k, v in temp_dict.items():
            if v == '':
                del filter_dict[k]
        for i in ['page', 'limit']:
            if i in filter_dict.keys():
                del filter_dict[i]
        queryset, filter_dict = deal_special_params(request, queryset, filter_dict)
        queryset = queryset.filter(**filter_dict)
        queryset = get_extra_value(request, queryset)
        total = queryset.count()
        r = queryset[(page - 1) * limit:page * limit]
        if r is not None:
            r = list(r.values())
            return Response({'data': r, 'page': page, 'limit': limit, 'total': total}, 200)
    return Response({'detail': '未分页'}, 400)


# 获取单个对象方法
def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    r = serializer.data
    for i in instance._meta.fields:
        if type(i) == models.fields.DateTimeField:
            if v := instance.__dict__[i.name]:
                r[i.name] = deal_value(v)
    return Response(r)


# 创建方法
def create(self, request, *args, **kwargs):
    if request.user.is_super:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance._meta.object_name == 'User':
            instance.set_password(instance.password)
            headers = self.get_success_headers(serializer.data)
        instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    dept_belong_id = getattr(request.user, 'dept_belong_id', None)
    if not dept_belong_id:
        return Response({'detail': '没有数据权限'}, status=400, headers=headers)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    fields = []
    for field in instance._meta.fields:
        fields.append(field.name)
    if "dept_belong_id" in fields:
        instance.dept_belong_id = dept_belong_id
    if "creator_id" in fields:
        instance.creator_id = request.user.id
    if instance._meta.object_name == 'User':
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
    if request.user.is_super:
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        user = request.user
        roles = user.role.all()
        depts = set()
        for i in roles:
            for j in i.dept.all():
                print(j)
                depts.add(j.i)
        if instance.dept_belong_id in depts:
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data, 200)
        else:
            return Response({'detail': '没有修改权限'}, 400)


# 删除方法
def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if request.user.is_super:
        self.perform_destroy(instance)
        return Response({'detail': '删除成功'}, 200)
    else:
        user = request.user
        roles = user.role.all()
        depts = set()
        for i in roles:
            for j in i.dept.all():
                print(j)
                depts.add(j.i)
        if instance.dept_belong_id in depts:
            self.perform_destroy(instance)
            return Response({'detail': '删除成功'}, 200)
        else:
            return Response({'detail': '没有删除权限'}, 400)


# 多项更新
@action(['PUT'], url_path='mult_update', url_name='mult_update', detail=False)
def mult_update(self, request: HttpRequest, *args, **kwargs):
    id_list = request.GET.getlist('id[]')
    querys = request.POST.dict()
    queryset: QuerySet = self.get_queryset()
    queryset = queryset.filter(id__in=id_list)
    r = queryset.update(**querys)  # TODO:queryset 批量更新
    return Response({'msg': '批量修改成功成功', 'data': r}, 200)


# TODO:数据导出
@action(['POST'], url_path='export', url_name='export', detail=False)
def export(self, request: HttpRequest, *args, **kwargs):
    filter_dict = request.data
    temp_dict = request.data
    columns = [i for i in request.data.get('columns') if i['show']]
    fields = [i['prop'] for i in columns]
    for k, v in temp_dict.items():
        if v == '':
            del filter_dict[k]
    for i in ['page', 'limit', 'columns']:
        if i in filter_dict.keys():
            del filter_dict[i]
    queryset: QuerySet = self.get_queryset()
    queryset = deal_permission(request, queryset)
    queryset, filter_dict = deal_special_params(request, queryset, filter_dict)
    queryset = queryset.filter(**filter_dict)
    queryset = get_extra_value(request, queryset)

    r = queryset.values_list(*fields)
    d = pd.DataFrame(list(r), columns=[i['label'] for i in columns])
    p = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/")
    filename = queryset.model._meta.model_name + str(int(time.time() * 1000))
    d.to_excel(f'{p}/media/export/{filename}.xlsx', encoding='gb18030')
    return Response({'url': f'media/export/{filename}.xlsx'}, status=200)


# 字段处理
def deal_value(v):
    if type(v) == datetime.datetime:  #TODO:request- 处理时间
        # v = timezone.localtime(v)  # 获取时区为当前时区的时间; 时间=时间值+时区
        return timezone.datetime.strftime(v, "%Y-%m-%d %H:%M:%S")  #获取时间的时间值
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
        indexes = range(len(names))
        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size):
            yield {names[i] if '_id' not in names[i] else names[i].rstrip('_id'): deal_value(row[i]) for i in indexes}  #TODO:request-QuerySet修改values  去掉_id


# 自定义queryset
class MyQuerySet(QuerySet):

    def values(self, *fields, **expressions):  #TODO:QuerySet-values实现
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
                # 'queryset': m.objects.all(),
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
        "url": "Dept",  # restful链接基础url
        "label": "部门",
        "viewset": model_viewset(Dept, (ModelViewSet, ), (ModelSerializer, ))  # 对应视图集
    },
    {
        "url": "File",
        "label": "文件",
        "viewset": model_viewset(File, (ModelViewSet, ), (ModelSerializer, ))
    },
    {
        "url": "Menu",
        "label": "菜单",
        "viewset": model_viewset(Menu, (ModelViewSet, ), (ModelSerializer, ))
    },
    {
        "url": "Role",
        "label": "角色",
        "viewset": model_viewset(Role, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[SuperPermisssion])
    },
    {
        "url": "User",
        "label": "用户",
        "viewset": model_viewset(User, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[SuperPermisssion])
    },
    {
        "url": "LoginLog",
        "label": "日志",
        "viewset": model_viewset(LoginLog, (ModelViewSet, ), (ModelSerializer, ))
    },
    {
        "url": "Area",
        "label": "区域",
        "viewset": model_viewset(Area, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[])
    },
    {
        "url": "MenuInterface",
        "label": "接口",
        "viewset": model_viewset(MenuInterface, (ModelViewSet, ), (ModelSerializer, ), permission_classes=[SuperPermisssion])
    },
    {
        "url": "Enterprise",
        "label": "企业",
        "viewset": model_viewset(Enterprise, (ModelViewSet, ), (ModelSerializer, ))
    },
]
