from rest_framework import permissions
import re
from .models import user, role

white_api = ['/']


#TODO:自定义接口权限
class UrlPermisssion(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):  # 过滤所有请求, 接口权限
        # id = request.META.get('HTTP_UID')  #TODO:header中的uid值
        # ip = request.META.get('REMOTE_ADDR')  #TODO:获取ip
        if request.path in white_api:
            return True
        if request.user.is_super:
            return True
        roles = role.objects.filter(id__in=request.user.role)
        for i in roles:
            for j in i.menu_interface.all():
                if re.match(j.path.replace('{id}', '.*?'), request.path.lower()):  # 之所以id用{id}代表是因为drf_yasg生成的接口数据就是这样的
                    return True
        return False


class SuperPermisssion(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_super:
            return True
        return False

    def has_permission(self, request, view):  # 过滤所有请求
        if request.user.is_super:
            return True
        roles = role.objects.filter(id__in=request.user.role)
        for i in roles:
            if i.is_admin:
                return True
        return False
