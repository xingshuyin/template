from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from django.utils.translation import gettext_lazy as _


class MyJWTAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token):
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

        raise InvalidToken({
            #TODO:JWT-无效token提示
            # "detail": _("Given token not valid for any token type"),
            "detail": "登录已过期,请重新登陆.",
            # "messages": messages,
        })

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            # raise AuthenticationFailed(_("User not found"), code="user_not_found")
            raise AuthenticationFailed(_("用户不存在!"), code="user_not_found")

        if not user.is_active:
            # raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
            raise AuthenticationFailed(_("用户未激活!"), code="user_inactive")

        return user
