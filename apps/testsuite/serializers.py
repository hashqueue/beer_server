# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from rest_framework import serializers

from utils.drf_utils.base_model_serializer import BaseModelSerializer
from .models import TestSuite


class TestSuiteSerializer(BaseModelSerializer):
    class Meta:
        model = TestSuite
        fields = '__all__'
        read_only_fields = ('creator', 'modifier')


class RunTestSuiteSerializer(serializers.ModelSerializer):
    config_id = serializers.IntegerField(required=False, write_only=True, help_text='运行测试套件时使用的配置项ID',
                                         label='运行测试套件时使用的配置项ID')

    class Meta:
        model = TestSuite
        fields = ('id', 'config_id')
