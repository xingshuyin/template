import os
import sys
from pathlib import Path

import django
import pandas as pd
# from faker import Faker
# TODO:通过倒推父级目录得到项目目录
p = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/")
print(p)
# sys.path.append(r'/home/voc_python/backend')  # 将项目路径添加到系统搜寻路径当中
sys.path.append(p)  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'root.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置
# TODO:初始化数据
from system.models import *
# from system.views.data import Data
# import system.views.data as data_
# 循环引用, 可以另一个引用了被循环0引用的, 比如 system.views.data 已经被 system.urls 引用, 而本文件已经引用了system.urls 就可以从 system.urls 引用system.views.data 而不是直接引用他
from system.urls import urlpatterns, data_
from django.urls import get_resolver, resolve
# resolver = get_resolver()
# patterns = resolver.url_patterns


def init_user():
    l = [
        {
            'id': 1,
            # 'name': '管理员',
            'username': 'admin',
            'password': 'admin',
            'is_super': True
        },
        {
            'id': 2,
            # 'name': '用户',
            'username': 'user',
            'password': 'user',
            'is_super': False
        },
    ]  #
    for i in l:
        u = user.objects.create_user(**i)
        user_info.objects.create(user=u)


# 所有菜单路由都是子路由, 所以path不加/ (element-plus的menu组件)
def init_menu():
    l = [
        {
            'id': 1,
            'parent_id': None,
            'label': '系统管理',
            'icon': 'Operation',
            'component': '',
            'name': 'system',
            'path': 'system',
            'sort': 100,
            'is_link': False,
            'is_catalog': True
        },
        {
            'id': 2,
            'parent_id': 1,
            'label': '用户管理',
            'icon': 'CameraFilled',
            'component': 'system/user.vue',
            'name': 'user',
            'path': 'user',
            'sort': 1,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 3,
            'parent_id': 1,
            'label': '角色管理',
            'icon': 'userFilled',
            'component': 'system/role.vue',
            'name': 'role',
            'path': 'role',
            'sort': 2,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 4,
            'parent_id': 1,
            'label': '接口管理',
            'icon': 'WindPower',
            'component': 'system/interface.vue',
            'name': 'interface',
            'path': 'interface',
            'sort': 54,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 5,
            'parent_id': 1,
            'label': '部门管理',
            'icon': 'Guide',
            'component': 'system/dept.vue',
            'name': 'dept',
            'path': 'dept',
            'sort': 3,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 6,
            'parent_id': 1,
            'label': '菜单管理',
            'icon': 'Grid',
            'component': 'system/menu.vue',
            'name': 'menu',
            'path': 'menu',
            'sort': 1,
            'is_link': False,
            'is_catalog': False
        },

        {
            'id': 7,
            'parent_id': 1,
            'label': '登陆日志',
            'icon': 'List',
            'component': 'system/login_log.vue',
            'name': 'login_log',
            'path': 'login_log',
            'sort': 10,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 8,
            'parent_id': 1,
            'label': '文件管理',
            'icon': 'Folder',
            'component': 'system/file.vue',
            'name': 'file',
            'path': 'file',
            'sort': 10,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 9,
            'parent_id': None,
            'label': '字典管理',
            'icon': 'Operation',
            'component': '',
            'name': 'dict',
            'path': 'dict',
            'sort': 110,
            'is_link': False,
            'is_catalog': True
        },
        {
            'id': 10,
            'parent_id': 9,
            'label': '区域管理',
            'icon': 'Operation',
            'component': 'dict/area.vue',
            'name': 'area',
            'path': 'area',
            'sort': 1,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 10001,
            'parent_id': None,
            'label': '文章管理',
            'icon': 'Document',
            'component': 'admin/article.vue',
            'name': 'article',
            'path': 'article',
            'sort': 1,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 10002,
            'parent_id': None,
            'label': '爬虫管理',
            'icon': 'Document',
            'component': 'admin/spider.vue',
            'name': 'spider',
            'path': 'spider',
            'sort': 1,
            'is_link': False,
            'is_catalog': False
        },
        {
            'id': 10003,
            'parent_id': None,
            'label': '企业管理',
            'icon': 'Grid',
            'component': 'admin/enterprise.vue',
            'name': 'enterprise',
            'path': 'enterprise',
            'sort': 1,
            'is_link': False,
            'is_catalog': False
        },
    ]
    for i in l:
        print(i)
        menu.objects.update_or_create(defaults=i, **i)


METHOD_CHOICES = (
    (0, "GET"),
    (1, "POST"),
    (2, "PUT"),
    (3, "DELETE"),
)

METHOD_NAMES = {
    'get': '查询',
    'post': '添加',
    'put': '修改',
}
METHOD_NAMES_DETAIL = {
    'get': '获取',
    'put': '修改',
    'delete': '删除',
}
METHOD_NUMS = {
    'get': 0,
    'put': 2,
    'post': 1,
    'delete': 3,
}


def init_interface():
    # print(urlpatterns[0].pattern,urlpatterns[0].name )

    for pattern in urlpatterns:
        # print(pattern.callback.cls.model_name)
        # match = resolve(pattern.pattern)
        if "(?P<pk>[^/.]+)" in str(pattern.pattern):
            names = METHOD_NAMES_DETAIL
        else:
            names = METHOD_NAMES

        if pattern.callback.cls == data_.Data:
            for i in pattern.callback.actions.keys():
                method_num = METHOD_NUMS[i]
                model_name_ = 'data'
                print(pattern.name, model_name_ + '-' + pattern.callback.actions[i], pattern.pattern, pattern.callback.cls.model_name, method_num)

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
                    print(model_name + '-' + method_name, model_name_ + '-' + pattern.callback.actions[i], pattern.pattern, model_name, method_num)
                    interface.objects.update_or_create(defaults={'name': model_name + '-' + method_name, 'key': model_name_ + '-' + pattern.callback.actions[i], 'method': method_num, 'path': pattern.pattern, 'model': model_name_, 'model_name': model_name},
                                                       name=model_name + '-' + method_name, key=model_name_ + '-' + pattern.callback.actions[i], method=method_num, path=pattern.pattern, model=model_name_)

    return
    menus = menu.objects.all()
    for m in menus:
        n = m._meta.object_name
        print(m.name)

        for i in [['add', '添加', 1, "/" + m.name + "/"], ['delete', '删除', 3, "/" + m.name + "/{id}/"], ['put', '修改', 2, "/" + m.name + "/{id}/"], ['list', '查询', 0, "/" + m.name + "/"]]:
            interface.objects.update_or_create(defaults={'name': m.label + '_' + i[1], 'key': m.name + '_' + i[0], 'method': i[2], 'path': i[3], 'menu': m},
                                               name=m.label + '_' + i[1], key=m.name + '_' + i[0], method=i[2], path=i[3], menu=m)


def init_role():
    for i in [{'id': 1, "name": '管理员', "key": 'admin', 'is_admin': True, 'permission': 3},
              {'id': 2, "name": '匿名用户', "key": 'AnonymousUser', 'is_admin': False, 'permission': 0}]:
        r = role.objects.update_or_create(defaults=i, **i)
        if i['is_admin']:
            r[0].interface.set(interface.objects.all())
    admin = user.objects.get(id=1)
    admin.role = [1]
    admin.save()
    admin.role


def init_area():
    from django.db import connection
    from system.init.area import areas
    from system.models import area
    if area.objects.count() == 0:
        with connection.cursor() as cursor:
            for i in areas.split(";"):
                print(i)
                if len(i) > 5:
                    cursor.execute(i)


def init_spider():
    ...
    # from django.db import connection
    # from system.init.spider import spider
    # with connection.cursor() as cursor:
    #     for i in spider.split(";"):
    #         print(i)
    #         if len(i) > 5:
    #             cursor.execute(i)


def init():

    init_user()
    init_menu()
    init_interface()
    init_role()
    init_area()
    # init_spider()


if __name__ == '__main__':
    init()  # TODO:初始化数据
