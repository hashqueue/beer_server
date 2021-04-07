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
router.register(prefix=r'projects', viewset=ProjectsViewSet)
urlpatterns = [path('', include(router.urls)), ]

