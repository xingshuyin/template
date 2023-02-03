from django.urls import path
from .views.views_model import view_list
from rest_framework.routers import SimpleRouter
from .views.data import Data

router = SimpleRouter()  # TODO:DRF-创建router
for view in view_list:
    router.register(view['url'], view['viewset'])  # TODO:DRF-注册路由
router.register(prefix='data', viewset=Data, basename='data')
urlpatterns = [
    # path('sign/', signin)
]
urlpatterns += router.urls  # TODO:DRF-添加路由
