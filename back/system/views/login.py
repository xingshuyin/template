'''
Filename     : login.py
Description  : wjt-后端-登录接口
Author       : xingshuyin xingshuyin@outlook.com
Date         : 2022-09-30 16:16:26
LastEditors  : xingshuyin xingshuyin@outlook.com
LastEditTime : 2022-11-20 09:00:27
Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
'''
import hashlib
import threading
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainSerializer, PasswordField
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.utils import format_lazy, datetime_from_epoch
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..models import user, log
from ..utils import save_login_log


class MyAccessToken(AccessToken):

    def check_exp(self, claim="exp", current_time=None):
        """
        Checks whether a timestamp value in the given claim has passed (since
        the given datetime value in `current_time`).  Raises a TokenError with
        a user-facing error message if so.
        """
        if current_time is None:
            current_time = self.current_time

        try:
            claim_value = self.payload[claim]
        except KeyError:
            raise TokenError(format_lazy(_("Token has no '{}' claim"), claim))

        claim_time = datetime_from_epoch(claim_value)
        leeway = self.get_token_backend().get_leeway()
        if claim_time <= current_time - leeway:
            # raise TokenError(format_lazy(_("Token '{}' claim has expired"), claim))
            #TODO:JWT-token过期提示
            raise TokenError("登录已过期,请重新登陆.")


class MyRefreshToken(RefreshToken):
    access_token_class = MyAccessToken


def login_log(request):
    save_login_log(request)
    request.user.last_login = timezone.now()  # validate之后才能访问self.user
    request.user.save()


# TODO:JWT-获取token的序列化器
# 获取token就相当于登录
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html  手动创建令牌
class MyTokenObtainSerializer(TokenObtainSerializer):
    token_class = MyRefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()
        self.fields["openid"] = serializers.CharField(allow_null=True, required=False)  # 添加微信openid字段

    class Meta:
        model = user
        fields = "__all__"
        read_only_fields = ["id"]

    @classmethod
    def get_token(cls, user):
        # token = super().get_token(user)
        token = MyRefreshToken.for_user(user)  # TODO:手动获取token
        # Add custom claims
        # token['is_super'] = user.is_super
        # ...

        return token

    def validate(self, attrs):

        # attrs 为账号密码 ->  OrderedDict([('username', 'admin'), ('password', '123456')])

        if 'openid' in attrs.keys() and attrs['openid']:  # TODO:微信id登陆,小程序登陆
            if users := user.objects.filter(openid=attrs['openid']):
                self.user = users.first()
            else:
                raise exceptions.AuthenticationFailed(
                    '用户不存在',
                    "no_active_account",
                )
            data = {}
        else:
            # 之所以用hashlib 加密, 是因为在创建用户时也是用了这个加密
            attrs['password'] = hashlib.md5(attrs['password'].encode(encoding="UTF-8")).hexdigest()  # 把密码变成和创建用户时一样的形式, 但是数据库里储存并不是这个, 而是再次用密钥加密后的
            data = self.my_super_validate(attrs)  # 简单来说,就是对比数据库的用户名和加密后的密码, 通过了获取登陆用户并赋值给self.user
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        request = self.context.get("request")  # 获取请求对象
        request.user = self.user
        t1 = threading.Thread(target=login_log, args=(request, ))
        t1.start()
        # data['user'] = {'username': self.user.username, 'uid': self.user.id}
        # self.user.last_login = timezone.now()  # validate之后才能访问self.user

        # save_login_log(request)
        # self.user.save()

        return data

    def my_super_validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass
        self.user = authenticate(**authenticate_kwargs)  # 这块可以手动比较用户名和密码,然后自己获取用户实例并赋值给self.user
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            # TODO:JWT-验证失败时返回的detail信息
            raise exceptions.AuthenticationFailed(
                '账号或密码错误',
                "no_active_account",
            )
        return {}


# TODO:刷新token的序列化器
class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = MyRefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)
        return data


# 获取token视图集
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from rest_framework.response import Response
        from rest_framework import generics, status
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=False)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# 刷新token视图集
class MyTokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    serializer_class = MyTokenRefreshSerializer
