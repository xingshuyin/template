"""
Request工具类
"""
import json
import time

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.urls.resolvers import ResolverMatch
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_agents import parse
from functools import wraps
from django.conf import settings
from django_ratelimit import ALL, UNSAFE
from django_ratelimit.core import is_ratelimited
from .models import log
from rest_framework.response import Response


def get_request_user(request):
    """
    获取请求user
    (1)如果request里的user没有认证,那么则手动认证一次
    :param request:
    :return:
    """
    user: AbstractBaseUser = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user
    try:
        user, tokrn = JWTAuthentication().authenticate(request)
    except Exception as e:
        pass
    return user or AnonymousUser()


def get_request_ip(request):
    """
    获取请求IP
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
        return ip
    ip = request.META.get('REMOTE_ADDR', '') or getattr(request, 'request_ip', None)
    return ip or 'unknown'


def get_request_data(request):
    """
    获取请求参数
    :param request:
    :return:
    """
    request_data = getattr(request, 'request_data', None)
    if request_data:
        return request_data
    data: dict = {**request.GET.dict(), **request.POST.dict()}
    if not data:
        try:
            body = request.body
            if body:
                data = json.loads(body)
        except Exception as e:
            pass
        if not isinstance(data, dict):
            data = {'data': data}
    return data


def get_request_path(request, *args, **kwargs):
    """
    获取请求路径
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    request_path = getattr(request, 'request_path', None)
    if request_path:
        return request_path
    values = []
    for arg in args:
        if len(arg) == 0:
            continue
        if isinstance(arg, str):
            values.append(arg)
        elif isinstance(arg, (tuple, set, list)):
            values.extend(arg)
        elif isinstance(arg, dict):
            values.extend(arg.values())
    if len(values) == 0:
        return request.path
    path: str = request.path
    for value in values:
        path = path.replace('/' + value, '/' + '{id}')
    return path


def get_request_canonical_path(request, ):
    """
    获取请求路径
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    request_path = getattr(request, 'request_canonical_path', None)
    if request_path:
        return request_path
    path: str = request.path
    resolver_match: ResolverMatch = request.resolver_match
    for value in resolver_match.args:
        path = path.replace(f"/{value}", "/{id}")
    for key, value in resolver_match.kwargs.items():
        if key == 'pk':
            path = path.replace(f"/{value}", f"/{{id}}")
            continue
        path = path.replace(f"/{value}", f"/{{{key}}}")

    return path


def get_browser(request, ):
    """
    获取浏览器名
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    return user_agent.get_browser()


def get_os(request, ):
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    return user_agent.get_os()


def get_verbose_name(queryset=None, view=None, model=None):
    try:
        if queryset is not None and hasattr(queryset, 'model'):
            model = queryset.model
        elif view and hasattr(view.get_queryset(), 'model'):
            model = view.get_queryset().model
        elif view and hasattr(view.get_serializer(), 'Meta') and hasattr(view.get_serializer().Meta, 'model'):
            model = view.get_serializer().Meta.model
        if model:
            return getattr(model, '_meta').verbose_name
        else:
            model = queryset.model._meta.verbose_name
    except Exception as e:
        pass
    return model if model else ""


def get_ip_analysis(ip):
    data = {"continent": "", "country": "", "province": "", "city": "", "district": "", "isp": "",
            "area_code": "", "country_english": "", "country_code": "", "longitude": "", "latitude": ""}
    if ip != 'unknown' and ip:
        if getattr(settings, 'ENABLE_LOGIN_ANALYSIS_LOG', True):
            try:
                res = requests.get(url='https://ip.django-vue-admin.com/ip/analysis', params={"ip": ip}, timeout=5)
                if res.status_code == 200:
                    res_data = res.json()
                    if res_data.get('code') == 0:
                        data = res_data.get('data')
                return data
            except Exception as e:
                ...
    return data


def save_login_log(request):
    """
    保存登录日志
    :return:
    """
    ip = get_request_ip(request=request)
    analysis_data = get_ip_analysis(ip)
    analysis_data['username'] = request.user.name
    analysis_data['ip'] = ip
    analysis_data['agent'] = str(parse(request.META['HTTP_USER_AGENT']))
    analysis_data['browser'] = get_browser(request)
    analysis_data['os'] = get_os(request)
    analysis_data['creator'] = request.user.id
    analysis_data['dept_belong'] = getattr(request.user, 'dept_id', '')
    log.objects.create(**analysis_data)


def get_time(f):

    def inner(*args, **kwargs):
        start = time.time()
        r = f(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r

    return inner


# TODO:访问频率限制 （django-ratelimit）
def ratelimit(group=None, key=None, rate=None, method=ALL, block=True, msg='访问频率过快'):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(s, request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                # cls = getattr(
                #     settings, 'RATELIMIT_EXCEPTION_CLASS', Ratelimited)
                # print('-------------',cls)
                return Response({'detail': msg, 'data': []}, 403)
            return fn(s, request, *args, **kw)
        return _wrapped
    return decorator


ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE


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
