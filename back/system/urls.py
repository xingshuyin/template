from django.urls import path, get_resolver
from .views.views_model import view_list
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
import system.views.data as data_


class MyRouter(SimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


router = MyRouter()  # TODO:DRF-创建router
for view in view_list:
    router.register(view['url'], view['viewset'], view['label'])  # TODO:DRF-注册路由
router.register(prefix='data', viewset=data_.Data, basename='数据')
urlpatterns = [
    # path('sign/', signin)
]
urlpatterns += router.urls  # TODO:DRF-添加路由
