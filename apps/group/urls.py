# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:38
# @Author  : anonymous
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path, include
from rest_framework import routers

from .views import GroupsViewSet

router = routers.DefaultRouter()
router.register(prefix=r'groups', viewset=GroupsViewSet)
urlpatterns = [path('', include(router.urls)), ]

