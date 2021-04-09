# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from .models import TestCase, TestStep, TestStepParams, TestStepValidator


class TestStepParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStepParams
        exclude = ('teststep',)


class TestStepValidatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStepValidator
        exclude = ('teststep',)


class TestStepSerializer(WritableNestedModelSerializer):
    step_params = TestStepParamsSerializer(many=True, allow_null=True)
    step_validators = TestStepValidatorSerializer(many=True, allow_null=True)

    class Meta:
        model = TestStep
        exclude = ('testcase',)


class TestCaseSerializer(BaseModelSerializer, WritableNestedModelSerializer):
    teststeps = TestStepSerializer(many=True)

    class Meta:
        model = TestCase
        exclude = ('deleted',)
        read_only_fields = ('creator', 'modifier')
