# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:38
# @Author  : anonymous
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path, include
from rest_framework import routers

from .views import ConfigsViewSet

router = routers.DefaultRouter()
router.register(prefix=r'configs', viewset=ConfigsViewSet)
urlpatterns = [path('', include(router.urls)), ]
