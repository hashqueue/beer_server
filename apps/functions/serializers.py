# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from .models import Function


class FunctionSerializer(BaseModelSerializer):
    class Meta:
        model = Function
        fields = '__all__'
        read_only_fields = ('creator', 'modifier')
