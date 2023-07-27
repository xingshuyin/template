"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from root import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from system.views.login import MyTokenObtainPairView
from system.views.login import MyTokenRefreshView

schema_view = get_schema_view(  # TODO:swagger-创建view
    openapi.Info(
        title="接口文档",  # 必传
        default_version="v1",  # 必传
    ),
    public=True,
    authentication_classes=[JWTAuthentication])
urlpatterns = [
    path('', include('system.urls')),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger"),  # TODO:swagger-注册view路由
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # TODO:JWT--引入token视图
    path('refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),  # TODO:JWT--引入refresh视图
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # TODO:添加文件路由
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
