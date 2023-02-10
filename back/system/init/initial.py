# TODO:初始化数据
import os
from pathlib import Path
import sys

import django
import pandas as pd
from faker import Faker
# TODO:通过倒推父级目录得到项目目录
p = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/")

# sys.path.append(r'/home/voc_python/backend')  # 将项目路径添加到系统搜寻路径当中
sys.path.append(p)  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'root.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置
from system.models import *
'''
description: 初始化后端用户
return {*}
'''


def init_User():
    l = [
        {
            'name': '管理员',
            'username': 'admin',
            'password': 'admin',
            'is_super': True
        },
        {
            'name': '用户',
            'username': 'user',
            'password': 'user',
            'is_super': False
        },
    ]  #
    for i in l:
        User.objects.create_user(**i)


'''
description: 初始化菜单
return {*}
'''


# 所有菜单路由都是子路由, 所以path不加/ (element-plus的menu组件)
def init_Menu():
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
            'icon': 'UserFilled',
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
            'component': 'system/menu_interface.vue',
            'name': 'menu_interface',
            'path': 'menu_interface',
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
        {
            'id': 8,
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
            'id': 9,
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
    ]
    for i in l:
        print(i)
        Menu.objects.create(**i)


METHOD_CHOICES = (
    (0, "GET"),
    (1, "POST"),
    (2, "PUT"),
    (3, "DELETE"),
)


def init_MenuInterface():
    menus = Menu.objects.all()
    for m in menus:
        n = m._meta.object_name
        print(m.name)

        for i in [['add', '添加', 1, "/" + m.name + "/"], ['delete', '删除', 3, "/" + m.name + "/{id}/"], ['put', '修改', 2, "/" + m.name + "/{id}/"], ['list', '查询', 0, "/" + m.name + "/"]]:
            MenuInterface.objects.create(name=i[1], key=i[0], method=i[2], path=i[3], menu=m)


def init_Role():
    for i in [{"name": '管理员', "key": 'admin', 'is_admin': True, 'permission': 3}]:
        r = Role.objects.create(**i)


def init_area():
    from system.init.area import areas
    from django.db import connection
    with connection.cursor() as cursor:
        for i in areas.split(";"):
            print(i)
            if i:
                cursor.execute(i)


def init():
    # init_User()
    init_Menu()
    # init_MenuInterface()
    # init_Role()
    # init_area()


if __name__ == '__main__':
    init()  #TODO:初始化数据
