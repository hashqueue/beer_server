# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from .models import TestCase, TestStep, TestStepValidator


class TestStepValidatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStepValidator
        exclude = ('teststep',)


class TestStepSerializer(WritableNestedModelSerializer):
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


class RunTestCaseSerializer(BaseModelSerializer, WritableNestedModelSerializer):

    class Meta:
        model = TestCase
        exclude = ('deleted',)
        read_only_fields = ('creator', 'modifier', 'testcase_name', 'testcase_desc', 'testsuite')
