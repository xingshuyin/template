# TODO:初始化数据
import os
import sys
from pathlib import Path

import django
from system.models import *

# TODO:通过倒推父级目录得到项目目录
p = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/")

# sys.path.append(r'/home/voc_python/backend')  # 将项目路径添加到系统搜寻路径当中
sys.path.append(p)  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'root.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置


def init_user():
    l = [
        {
            'id': 1,
            'name': '管理员',
            'username': 'admin',
            'password': 'admin',
            'is_super': True
        },
        {
            'id': 2,
            'name': '用户',
            'username': 'user',
            'password': 'user',
            'is_super': False
        },
    ]  #
    for i in l:
        user.objects.create_user(**i)


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
        {
            'id': 10,
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
            'id': 11,
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
    ]
    for i in l:
        print(i)
        menu.objects.create(**i)


METHOD_CHOICES = (
    (0, "GET"),
    (1, "POST"),
    (2, "PUT"),
    (3, "DELETE"),
)


def init_menu_interface():
    menus = menu.objects.all()
    for m in menus:
        n = m._meta.object_name
        print(m.name)

        for i in [['add', '添加', 1, "/" + m.name + "/"], ['delete', '删除', 3, "/" + m.name + "/{id}/"], ['put', '修改', 2, "/" + m.name + "/{id}/"], ['list', '查询', 0, "/" + m.name + "/"]]:
            menu_interface.objects.create(
                name=m.label + '_' + i[1], key=m.name + '_' + i[0], method=i[2], path=i[3], menu=m)


def init_role():
    for i in [{'id': 1, "name": '管理员', "key": 'admin', 'is_admin': True, 'permission': 3}]:
        r = role.objects.create(**i)
    admin = user.objects.get(id=1)
    admin.role = [1]
    admin.save()


def init_area():
    from django.db import connection
    from system.init.area import areas
    with connection.cursor() as cursor:
        for i in areas.split(";"):
            print(i)
            if len(i) > 5:
                cursor.execute(i)


def init_spider():
    from django.db import connection
    from system.init.spider import spider
    with connection.cursor() as cursor:
        for i in spider.split(";"):
            print(i)
            if len(i) > 5:
                cursor.execute(i)


def init():
    init_user()
    init_menu()
    init_menu_interface()
    init_role()
    init_area()
    init_spider()


if __name__ == '__main__':
    init()  # TODO:初始化数据
