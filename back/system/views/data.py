'''
Filename     : data.py
Description  : wjt-后端-非restful规范接口
Author       : xingshuyin xingshuyin@outlook.com
Date         : 2022-10-03 12:14:32
LastEditors  : xingshuyin xingshuyin@outlook.com
LastEditTime : 2022-11-30 12:56:18
Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
'''
from pathlib import Path
from django.forms import CharField, model_to_dict
from system.models import *
from django.utils._os import safe_join
from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
# from django.db.models import Count, F, Value, CharField
# import datetime
from django.db.models.functions import Concat
from django.views.decorators.cache import cache_page
from django.utils import timezone
from .views_model import MyQuerySet
import os
import hashlib
from ..permission import SuperPermisssion


def ranges():
    """
    :function: 获取本周周一日期
    :param today:
    :return: 返回周一的日期
    :return_type: string
    """
    # now = timezone.now()  # 不要用datetime的now不然会出现警告
    # this_week_start = now - timedelta(days=now.weekday())
    # this_month_start = timezone.make_aware(datetime.datetime(now.year, now.month, 1))
    # this_year_start = timezone.make_aware(datetime.datetime(now.year, 1, 1))
    now = timezone.now()  # 不要用datetime的now不然会出现警告
    this_week_start = now - timezone.timedelta(days=now.weekday())
    this_month_start = timezone.datetime(now.year, now.month, 1)
    this_year_start = timezone.datetime(now.year, 1, 1)
    return [now, this_week_start, this_month_start, this_year_start]


# fetch结果转换为键值对形式
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_all_sub_dept(dept_id):
    r = [dept_id]
    childern = dept.objects.filter(parent__id=dept_id)
    if len(childern):
        for i in childern:
            r.extend(get_all_sub_dept(i.id))
    return r


def get_dept_permission(request, dept_id, permission):
    if permission == 0:
        return []
    elif permission == 1:
        return get_all_sub_dept(dept_id)
    elif permission == 2:
        return [dept_id]
    elif permission == 3:
        return []
    elif permission == 4:
        return request.data['custom_dept']


class Data(ViewSet):
    # 文件上传接口
    @action(['post'], url_path='upload', url_name='upload', detail=False, permission_classes=[])
    def upload(self, request: Request):  #TODO:文件上传-上传接口
        print(request.FILES['file'].name)  # 上传文件以file为key值
        form = FileForm({'name': request.FILES['file'].name}, request.FILES)
        if form.is_valid():
            f = form.save()
            return JsonResponse({'id': f.id, 'name': f.name, 'url': f.file.url})
        print(form)
        return JsonResponse({'msg': '格式验证失败', 'data': form.data})

    # # 文件删除接口(已使用文件表删除)
    # @action(['post'], url_path='remove', url_name='remove', detail=False, permission_classes=[])
    # def remove(self, request: Request):
    #     file_path = request.data.get('file')
    #     if file_path.startswith('media'):
    #         print('删除文件', file_path)
    #         real_path = safe_join(settings.MEDIA_ROOT, file_path.lstrip(settings.MEDIA_URL.lstrip('/')))
    #         try:
    #             if os.path.isdir(real_path):
    #                 os.rmdir(real_path)
    #             else:
    #                 os.remove(real_path)
    #             return JsonResponse({'msg': '删除文件成功', 'code': 200, 'data': {'path': real_path}})
    #         except FileNotFoundError:
    #             # FileNotFoundError is raised if the file or directory was removed
    #             # concurrently.
    #             return JsonResponse({'msg': '格式验证失败', 'data': {}})

    # 获取所有菜单 及对应接口
    @action(['get'], url_path='GetAllMenu', url_name='GetAllMenu', detail=False, permission_classes=[SuperPermisssion])
    def GetAllMenu(self, request: Request):
        interfaces = MyQuerySet(menu_interface)
        menus = list(MyQuerySet(menu).values())
        for i in menus:
            i['interfaces'] = list(interfaces.filter(menu__id=i['id']).values())
        return JsonResponse(menus, safe=False)

    # 获取角色权限 及接口权限
    @action(['get'], url_path='GetRolePermision', url_name='GetRolePermision', detail=False, permission_classes=[])
    def GetRolePermision(self, request: Request):
        role_id = request.GET.get('role_id')
        role = role.objects.get(id=role_id)
        menus = [i.id for i in role.menu.all()]
        interfaces = [i.id for i in role.menu_interface.all()]
        return JsonResponse({'interfaces': interfaces, 'menus': menus, 'permission': role.permission}, safe=False)

    # 设置角色权限
    @action(['post'], url_path='SetRolePermision', url_name='SetRolePermision', detail=False, permission_classes=[SuperPermisssion])
    def SetRolePermision(self, request: Request):
        interfaces = request.data['interfaces']
        permission = request.data['permission']
        menus = request.data['menus']
        role_id = request.data['role_id']
        role = role.objects.get(id=role_id)
        role.permission = permission
        role.menu.set(menus)  # TODO:request-多对多 覆盖值
        role.menu_interface.set(interfaces)
        role.save()
        return JsonResponse({'msg': '设置成功'})

    # 获取菜单
    @action(['get'], url_path='GetMenu', url_name='GetMenu', detail=False, permission_classes=[])
    def GetMenu(self, request: Request):
        # try:
        user = request.user
        if user.is_super:
            menus = list(MyQuerySet(menu).values())
        else:
            menus_set = set()
            menus = []
            for i in user.role:
                for j in list(role.objects.get(id=i).menu.values()):
                    if j['id'] not in menus_set:
                        menus.append(j)
                        menus_set.add(j['id'])
        return JsonResponse(list(menus), safe=False)

    # 获取角色列表
    @action(['get'], url_path='GetAllRoleDict', url_name='GetAllRoleDict', detail=False, permission_classes=[])
    def GetAllRoleDict(self, request: Request):
        filter_dict = request.GET.dict()
        roles = MyQuerySet(role).filter(**filter_dict).values(
            'id',
            'name',
        )
        return Response({i['id']: i for i in list(roles)}, 200)

    # 获取用户信息
    @action(['get'], url_path='get_userinfo', url_name='get_userinfo', detail=False, permission_classes=[])
    def get_userinfo(self, request: Request):
        user = request.user
        r = model_to_dict(user)
        del r['password']
        del r['role']
        return JsonResponse(r, safe=False)

    # 修改密码
    @action(['post'], url_path='change_password', url_name='change_password', detail=False, permission_classes=[])
    def change_password(self, request: Request):
        user = request.user
        new_password = request.data.get("new_password")
        old_password = request.data.get("old_password")
        from django.contrib.auth import authenticate
        mm_user = authenticate(username=user.username, password=hashlib.md5(old_password.encode(encoding="UTF-8")).hexdigest())
        if mm_user:
            user.set_password(new_password)
            user.save()
            return JsonResponse({'code': 200, 'msg': '密码修改成功'}, safe=False)
        else:
            return JsonResponse({'code': 400, 'msg': '旧密码错误'}, safe=False)

    # 获取压缩图片
    @action(['get'], url_path='zip_img', url_name='zip_img', detail=True, permission_classes=[])
    def zip_img(self, request: Request, pk):
        p = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/")
        zip_path = f'{p}/media/img_zip/{pk}.jpg'
        if not os.path.exists(zip_path):
            f = file.objects.get(id=pk)
            from PIL import Image
            path = f.file.path
            im = Image.open(path)
            im.save(zip_path, quality=7)  # quality 是压缩比率, 值越小图片越小
        # r = open(zip_path, "rb")
        return FileResponse(open(zip_path, "rb"))
        # return HttpResponse(r.read(), content_type='image/jpg')
