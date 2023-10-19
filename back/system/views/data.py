from pathlib import Path
import zipfile
from django.db.models import Q, F
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
from ..utils import METHOD_NAMES, METHOD_NAMES_DETAIL, METHOD_NUMS, ratelimit
import system.urls as urls
from django.db import transaction


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
    model_name = "数据"
    # 文件上传接口

    @action(['post'], url_path='upload', url_name='文件上传', detail=False, permission_classes=[LoginPermisssion])
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
    @action(['get'], url_path='GetAllMenu', url_name='获取所有菜单', detail=False, permission_classes=[SuperPermisssion])
    def GetAllMenu(self, request: Request):
        interfaces = MyQuerySet(interface)
        menus = list(MyQuerySet(menu).values())
        # for i in menus:
        #     i['interfaces'] = list(interfaces.filter(menu__id=i['id']).values())
        return Response(menus, status=200)

    # 获取角色权限 及接口权限
    @action(['get'], url_path='GetRolePermision', url_name='获取角色权限', detail=False, permission_classes=[LoginPermisssion])
    def GetRolePermision(self, request: Request):
        role_id = request.GET.get('role_id')
        ro = role.objects.get(id=role_id)
        menus = [i.id for i in ro.menu.all()]
        interfaces = [i.id for i in ro.interface.all()]
        return Response({'interfaces': interfaces, 'menus': menus, 'permission': ro.permission}, status=200)

    # 设置角色权限
    @action(['post'], url_path='SetRolePermision', url_name='设置角色权限', detail=False, permission_classes=[SuperPermisssion, UrlPermisssion])
    def SetRolePermision(self, request: Request):
        interfaces = request.data['interfaces']
        permission = request.data['permission']
        menus = request.data['menus']
        role_id = request.data['role_id']
        ro = role.objects.get(id=role_id)
        ro.permission = permission
        ro.menu.set(menus)  # TODO:request-多对多 覆盖值
        ro.interface.set(interfaces)
        ro.save()
        return Response({'detail': '设置成功'}, status=200)

    # 获取菜单
    @action(['get'], url_path='GetMenu', url_name='获取菜单', detail=False, permission_classes=[LoginPermisssion])
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
    @action(['get'], url_path='GetAllRoleDict', url_name='获取角色列表', detail=False, permission_classes=[LoginPermisssion])
    def GetAllRoleDict(self, request: Request):
        filter_dict = request.GET.dict()
        roles = MyQuerySet(role).filter(**filter_dict).values(
            'id',
            'name',
        )
        return Response({i['id']: i for i in list(roles)}, 200)

    # 获取用户信息
    @action(['get'], url_path='get_userinfo', url_name='获取用户信息', detail=False, permission_classes=[LoginPermisssion])
    def get_userinfo(self, request: Request):
        user = request.user
        user_info_ = user_info.objects.filter(user=user).first()
        user_info_ = user_info_.model_to_dict(deep=0)
        role_list = user.role
        interfaces = []
        for role_ in role_list:
            # 判断用户是否为超级管理员角色/如果拥有[全部数据权限]则返回所有数据
            role_item = role.objects.get(id=role_)
            interfaces.extend(list(role_item.interface.all().values_list('key')))
        interfaces = list(set([i[0] for i in interfaces]))
        user_info_['interfaces'] = interfaces
        user_info_['is_super'] = user.is_super
        user_info_['username'] = user.username
        return Response(user_info_, status=200)

    # 修改密码
    @action(['post'], url_path='change_password', url_name='修改密码', detail=False, permission_classes=[LoginPermisssion])
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
    @action(['get'], url_path='zip_img', url_name='获取压缩图片', detail=True, permission_classes=[])
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
    @action(['get'], url_path='temp', url_name='临时文件下载', detail=True, permission_classes=[])
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
    @transaction.atomic
    @action(['get'], url_path='init_permision', detail=False, url_name='生成接口', permission_classes=[SuperPermisssion])
    def init_permision(self, request: Request):


        for pattern in urls.urlpatterns:
            # print(pattern.callback.cls.model_name)
            # match = resolve(pattern.pattern)
            if "(?P<pk>[^/.]+)" in str(pattern.pattern):
                names = METHOD_NAMES_DETAIL
            else:
                names = METHOD_NAMES

            if pattern.callback.cls == Data:
                print(pattern.callback.actions)
                for i in pattern.callback.actions.keys():
                    if i in names.keys():
                        method_num = METHOD_NUMS[i]
                        model_name_ = 'data'
                        print(pattern.name, model_name_ + '-' + pattern.callback.actions[i],
                              pattern.pattern, pattern.callback.cls.model_name, method_num)

                        interface.objects.update_or_create(defaults={'name': pattern.name, 'key': model_name_ + '-' + pattern.callback.actions[i], 'method': method_num, 'path': pattern.pattern, 'model': model_name_, 'model_name': pattern.callback.cls.model_name},
                                                           name=pattern.name, key=model_name_ + '-' + pattern.callback.actions[i], method=method_num, path=pattern.pattern, model=model_name_)
            else:
                for i in pattern.callback.actions.keys():
                    if i in names.keys():
                        if 'list' in pattern.name or 'detail' in pattern.name:
                            method_name = names[i]
                        else:
                            method_name = pattern.name.split('-')[-1]
                        method_num = METHOD_NUMS[i]
                        model_name = pattern.callback.cls.model_name
                        model_name_ = pattern.callback.cls.queryset.model._meta.model_name
                        print(model_name + '-' + method_name, model_name_ + '-' +
                              pattern.callback.actions[i], pattern.pattern, model_name, method_num)
                        interface.objects.update_or_create(defaults={'name': model_name + '-' + method_name, 'key': model_name_ + '-' + pattern.callback.actions[i], 'method': method_num, 'path': pattern.pattern, 'model': model_name_, 'model_name': model_name},
                                                           name=model_name + '-' + method_name, key=model_name_ + '-' + pattern.callback.actions[i], method=method_num, path=pattern.pattern, model=model_name_)

        # menus = menu.objects.all()
        # for m in menus:
        #     n = m._meta.object_name
        #     for i in [['add', '添加', 1, "/" + m.name + "/"], ['delete', '删除', 3, "/" + m.name + "/{id}/"], ['put', '修改', 2, "/" + m.name + "/{id}/"], ['list', '查询', 0, "/" + m.name + "/"]]:
        #         interface.objects.update_or_create(defaults={'name': m.label + '_' + i[1], 'key': m.name + '_' + i[0], 'method': i[2]},
        #                                             name=m.label + '_' + i[1], key=m.name + '_' + i[0], method=i[2], path=i[3], menu=m)
        return Response({'detail': '接口初始化成功'}, status=200)

    # 注册
    @action(['post'], url_path='signin', url_name='注册', detail=False, permission_classes=[], authentication_classes=[])
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
                u_info= user_info.objects.create(user=u)
                u.set_password(u.password)
                u.name = u.username
                u.role.add(role.objects.get(key='normal'))
                u.save()
                return Response({"detail": "注册成功"}, status=200)
        else:
            return Response({"detail": "验证码错误"}, status=400)

    # 生成验证码
    @ratelimit(key='ip', rate='1/s')
    @action(['get'], url_path='captcha', url_name='生成验证码', detail=False, permission_classes=[], authentication_classes=[])
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


    @action(['get'], url_path='follow', detail=False, url_name='follow', permission_classes=[])
    def follow(self, request: Request):
        user = request.user

        type_ = request.GET.get('type')
        followed = request.GET.get('followed')
        print(followed, type(followed))
        id = request.GET.get('id')
        if type_ == 'user':
            if followed == 'false':
                user.user_info.follow_user.add(id)
            elif followed == 'true':
                user.follow_user.remove(id)

        
        return Response({'data': 'success'}, 200)
    @action(['get'], url_path='view', detail=False, url_name='view', permission_classes=[])
    def view(self, request: Request):
        type_ = request.GET.get('type')
        id = request.GET.get('id')
        if type_ == 'article':
            article_ = article.objects.get(id=id)
            article_.view = article_.view + 1
            article_.save()
            return Response({'data': article_.view}, 200)
        
    @action(['get'], url_path='like', detail=False, url_name='like', permission_classes=[])
    def like(self, request: Request):
        user = request.user
        type_ = request.GET.get('type')
        liked = request.GET.get('liked')
        id = request.GET.get('id')
        if type_ == 'article':
            if liked == 'false':
                user.user_info.article_like.add(id)
            elif liked == 'true':
                user.user_info.article_like.remove(id)
            return Response({'data': 'success'}, 200)   
        else:
            return Response({'data': 'like faild'}, 200)  
    @action(['get'], url_path='collect', detail=False, url_name='collect', permission_classes=[])
    def collect(self, request: Request):
        user = request.user
        type_ = request.GET.get('type')
        collected = request.GET.get('collected')
        id = request.GET.get('id')
        if type_ == 'article':
            if collected == 'false':
                user.user_info.article_collect.add(id)
            elif collected == 'true':
                user.user_info.article_collect.remove(id)
            return Response({'data': 'success'}, 200)       
        else:
            return Response({'data': 'collect faild'}, 200)  
        

    @action(['get'], url_path='article_comment', url_name='article_comment', detail=False, permission_classes=[], authentication_classes=[])
    def article_comment(self, request: Request): # 评论列表
        vid = request.GET.get('id')
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        queryset = MyQuerySet(article_comment).filter(article__id=vid, root=None).annotate(user_name=F('user__name'), user_icon=F('user__icon')).order_by(
            '-create_time',
            'root',
        )
        total = queryset.count()
        queryset = queryset[(page - 1) * limit:page * limit]
        r = []
        for i in list(queryset.values()):
            replys = MyQuerySet(article_comment).filter(root__id=i['id']).annotate(user_name=F('user__name'),
                                                                                   user_icon=F('user__icon'),
                                                                                   reply_user_name=F('reply__user__name'),
                                                                                   reply_user_icon=F('reply__user__icon')).order_by('-create_time')
            i['replys'] = list(replys.values())
            r.append(i)
        return Response({'data': r, 'total': total})
    
    @action(['get'], url_path='comment', url_name='comment', detail=False, permission_classes=[])
    def comment(self, request: Request): # 评论
        user = request.user
        filter_dict = request.GET.dict()
        if 'reply_id' in filter_dict.keys():
            if filter_dict['reply_id']:
                filter_dict['reply_id'] = int(filter_dict['reply_id'])
            else:
                filter_dict['reply_id'] = None
        if 'root_id' in filter_dict.keys():
            if  filter_dict['root_id']:
                filter_dict['root_id'] = int(filter_dict['root_id'])
            else:
                filter_dict['root_id'] = None
        del filter_dict['media_type']
        del filter_dict['media_id']
        media_type = request.GET.get('media_type')
        media_id = request.GET.get('media_id')
        if media_type == 'article':
            article_comment.objects.create(user_id=user.user_info.id, article_id=media_id, **filter_dict)
        return Response({})