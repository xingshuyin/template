from pathlib import Path
import zipfile
from django.forms import CharField, model_to_dict
from system.models import *
from django.utils._os import safe_join
from django.utils.encoding import escape_uri_path
from django.conf import settings
from django.core.cache import cache
from django.http import FileResponse, HttpResponse
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
from ..permission import SuperPermisssion, UrlPermisssion, LoginPermisssion
from io import BytesIO
from PIL import Image
import base64
from captcha.image import ImageCaptcha
from random import randint
from ..utils import ratelimit


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
    @action(['post'], url_path='upload', url_name='upload', detail=False, permission_classes=[LoginPermisssion])
    def upload(self, request: Request):  # TODO:文件上传-上传接口
        print(request.FILES['file'].name)  # 上传文件以file为key值
        form = FileForm({'name': request.FILES['file'].name}, request.FILES)
        if form.is_valid():
            f = form.save()
            return Response({'id': f.id, 'name': f.name, 'url': f.file.url})
        print(form)
        return Response({'detail': '格式验证失败', 'data': form.data}, 400)

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
    #             return Response({'msg': '删除文件成功', 'code': 200, 'data': {'path': real_path}})
    #         except FileNotFoundError:
    #             # FileNotFoundError is raised if the file or directory was removed
    #             # concurrently.
    #             return Response({'msg': '格式验证失败', 'data': {}})

    # 获取所有菜单 及对应接口
    @action(['get'], url_path='GetAllMenu', url_name='GetAllMenu', detail=False, permission_classes=[SuperPermisssion])
    def GetAllMenu(self, request: Request):
        interfaces = MyQuerySet(menu_interface)
        menus = list(MyQuerySet(menu).values())
        for i in menus:
            i['interfaces'] = list(interfaces.filter(menu__id=i['id']).values())
        return Response(menus, status=200)

    # 获取角色权限 及接口权限
    @action(['get'], url_path='GetRolePermision', url_name='GetRolePermision', detail=False, permission_classes=[LoginPermisssion])
    def GetRolePermision(self, request: Request):
        role_id = request.GET.get('role_id')
        ro = role.objects.get(id=role_id)
        menus = [i.id for i in ro.menu.all()]
        interfaces = [i.id for i in ro.menu_interface.all()]
        return Response({'interfaces': interfaces, 'menus': menus, 'permission': ro.permission}, status=200)

    # 设置角色权限
    @action(['post'], url_path='SetRolePermision', url_name='SetRolePermision', detail=False, permission_classes=[SuperPermisssion, UrlPermisssion])
    def SetRolePermision(self, request: Request):
        interfaces = request.data['interfaces']
        permission = request.data['permission']
        menus = request.data['menus']
        role_id = request.data['role_id']
        ro = role.objects.get(id=role_id)
        ro.permission = permission
        ro.menu.set(menus)  # TODO:request-多对多 覆盖值
        ro.menu_interface.set(interfaces)
        ro.save()
        return Response({'detail': '设置成功'}, status=200)

    # 获取菜单
    @action(['get'], url_path='GetMenu', url_name='GetMenu', detail=False, permission_classes=[LoginPermisssion])
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
        return Response(list(menus), status=200)

    # 获取角色列表
    @action(['get'], url_path='GetAllRoleDict', url_name='GetAllRoleDict', detail=False, permission_classes=[LoginPermisssion])
    def GetAllRoleDict(self, request: Request):
        filter_dict = request.GET.dict()
        roles = MyQuerySet(role).filter(**filter_dict).values(
            'id',
            'name',
        )
        return Response({i['id']: i for i in list(roles)}, 200)

    # 获取用户信息
    @action(['get'], url_path='get_userinfo', url_name='get_userinfo', detail=False, permission_classes=[LoginPermisssion])
    def get_userinfo(self, request: Request):
        user = request.user
        r = model_to_dict(user)
        role_list = user.role
        interfaces = []
        for role_ in role_list:
            # 判断用户是否为超级管理员角色/如果拥有[全部数据权限]则返回所有数据
            role_item = role.objects.get(id=role_)
            interfaces.extend(list(role_item.menu_interface.all().values_list('key')))
        interfaces = list(set([i[0] for i in interfaces]))
        r['interfaces'] = interfaces
        del r['password']
        del r['role']
        return Response(r, status=200)

    # 修改密码
    @action(['post'], url_path='change_password', url_name='change_password', detail=False, permission_classes=[LoginPermisssion])
    def change_password(self, request: Request):
        user = request.user
        new_password = request.data.get("new_password")
        old_password = request.data.get("old_password")
        from django.contrib.auth import authenticate
        mm_user = authenticate(username=user.username, password=hashlib.md5(old_password.encode(encoding="UTF-8")).hexdigest())
        if mm_user:
            user.set_password(new_password)
            user.save()
            return Response({'detail': '密码修改成功'}, status=200)
        else:
            return Response({'detail': '旧密码错误'}, status=400)

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

    # TODO:临时文件下载
    @action(['get'], url_path='temp', url_name='temp', detail=True, permission_classes=[])
    def temp(self, request: Request, pk):
        response = HttpResponse(content_type='application/octet-stream')
        zip_file = zipfile.ZipFile(response, 'w')
        zip_file.write(r"D:\python\template\back\system\init\spider.xlsx", 'spider')
        zip_file.write(r"D:\python\template\back\system\init\initial.py", 'initial')
        zip_file.close()
        response_name = 'spider' + '.zip'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(response_name))
        return response

    # 生成接口
    @action(['get'], url_path='init_permision', detail=False, url_name='init_permision', permission_classes=[SuperPermisssion])
    def init_permision(self, request: Request):
        menus = menu.objects.all()
        for m in menus:
            n = m._meta.object_name
            for i in [['add', '添加', 1, "/" + m.name + "/"], ['delete', '删除', 3, "/" + m.name + "/{id}/"], ['put', '修改', 2, "/" + m.name + "/{id}/"], ['list', '查询', 0, "/" + m.name + "/"]]:
                menu_interface.objects.update_or_create(defaults={'name': m.label + '_' + i[1], 'key': m.name + '_' + i[0], 'method': i[2]},
                                                        name=m.label + '_' + i[1], key=m.name + '_' + i[0], method=i[2], path=i[3], menu=m)
        return Response({'detail': '接口初始化成功'}, status=200)

    # 注册
    @action(['post'], url_path='signin', url_name='signin', detail=False, permission_classes=[], authentication_classes=[])
    def signin(self, request: Request):
        captcha = request.data.get("captcha")
        if captcha and captcha.lower() == cache.get('captcha-' + request.META.get('REMOTE_ADDR')).lower():
            username = request.data.get("username")
            password = request.data.get("password")
            user_ = user.objects.filter(username=username).first()
            if user_:
                return Response({"detail": "用户已存在"}, status=400)
            else:
                u = user.objects.create(username=username, password=password)
                u.set_password(u.password)
                u.name = u.username
                u.role.add(role.objects.get(key='normal'))
                u.save()
                return Response({"detail": "注册成功"}, status=200)
        else:
            return Response({"detail": "验证码错误"}, status=400)

    # 生成验证码
    @ratelimit(key='ip', rate='1/s')
    @action(['get'], url_path='captcha', url_name='captcha', detail=False, permission_classes=[], authentication_classes=[])
    def captcha(self, request: Request):

        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        chars = ''
        for i in range(4):
            chars += list[randint(0, len(list) - 1)]
        cache.set('captcha-' + request.META.get('REMOTE_ADDR'), chars, 60)
        image = ImageCaptcha(font_sizes=(42, 40, 46)).generate(chars)
        # 将图片写入BytesIO
        # img_io = BytesIO()
        # image.save(img_io, 'JPEG')  # 保存图片

        # # 从BytesIO中获取图片数据
        # img_byte = img_io.getvalue()

        # 将图片转换为base64格式
        img_base64 = base64.b64encode(image.getvalue())
        print(chars)
        return Response({"data": img_base64, 'detail': '成功'}, status=200)
