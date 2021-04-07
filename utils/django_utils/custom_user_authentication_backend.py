# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 下午12:15
# @Author  : anonymous
# @File    : custom_user_authentication_backend.py
# @Software: PyCharm
# @Description:
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class MyCustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
