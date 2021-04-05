# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 下午1:49
# @Author  : anonymous
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, GetAndUpdateCurrentLoginUserInfoView, UserRegisterView

urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('user/profile/<int:pk>/', GetAndUpdateCurrentLoginUserInfoView.as_view(), name='get_and_update_user_info'),
]
