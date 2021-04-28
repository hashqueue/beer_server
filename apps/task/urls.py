# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:38
# @Author  : anonymous
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path, include
from rest_framework import routers

from .views import TasksViewSet

router = routers.DefaultRouter()
router.register(prefix=r'tasks', viewset=TasksViewSet)
urlpatterns = [path('', include(router.urls)), ]

