from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AnonymousUser


class MyJWTAuthentication(JWTAuthentication):

    def authenticate(self, request, force=False):  # force=True 强制返回用户不报错, 没有用户就返回AnonymousUser, 用于手动验证用户(可能没有token), 'authentication_classes': [] 的接口
        header = self.get_header(request)
        force_header = request.headers.get('Http-Force', 'false') # 前端通过设置Http-Force的请求头为true来绕过登录验证, 相当于用匿名用户访问需要登录验证的接口,可以设置匿名用户角色(key=AnonymousUser)的权限以控制接口
        if force_header == 'true':
            force = True
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None and not force:
            return None

        validated_token = self.get_validated_token(raw_token, force)

        return self.get_user(validated_token, force), validated_token

    def get_validated_token(self, raw_token, force):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({
                    "token_class": AuthToken.__name__,
                    "token_type": AuthToken.token_type,
                    "message": e.args[0],
                })
        if force:
            return {}
        raise InvalidToken({
            # TODO:JWT-无效token提示
            # "detail": _("Given token not valid for any token type"),
            "detail": "登录已过期,请重新登陆.",
            # "messages": messages,
        })

    def get_user(self, validated_token, force):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            if force:
                user_id = 0
            else:
                raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            if force:
                user = AnonymousUser()
                user.is_active = True
            else:
                # raise AuthenticationFailed(_("User not found"), code="user_not_found")
                raise AuthenticationFailed(_("用户不存在!"), code="user_not_found")

        if not user.is_active:
            # raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
            raise AuthenticationFailed(_("用户未激活!"), code="user_inactive")

        return user
