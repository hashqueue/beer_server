# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:38
# @Author  : anonymous
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path, include
from rest_framework import routers

from .views import ProjectsViewSet

router = routers.DefaultRouter()
# 如果视图类中没有指定queryset，则需要手动指定basename
router.register(prefix=r'projects', viewset=ProjectsViewSet, basename='project')
urlpatterns = [path('', include(router.urls)), ]

