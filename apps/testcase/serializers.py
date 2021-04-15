# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from rest_framework.serializers import ModelSerializer
from utils.drf_utils.base_model_serializer import BaseModelSerializer
from .models import TestCase, TestStep, TestStepValidator


class TestStepValidatorSerializer(ModelSerializer):
    class Meta:
        model = TestStepValidator
        exclude = ('teststep',)


class TestStepSerializer(ModelSerializer):
    step_validators = TestStepValidatorSerializer(many=True, required=False)

    class Meta:
        model = TestStep
        exclude = ('testcase',)


class TestCaseSerializer(BaseModelSerializer):
    teststeps = TestStepSerializer(many=True)

    class Meta:
        model = TestCase
        fields = '__all__'
        read_only_fields = ('creator', 'modifier')

    def create(self, validated_data):
        teststeps_data = validated_data.pop('teststeps', False)
        testcase = TestCase.objects.create(**validated_data)
        if teststeps_data:
            for teststep_data in teststeps_data:
                step_validators_data = teststep_data.pop('step_validators', False)
                teststep = TestStep.objects.create(testcase=testcase, **teststep_data)
                if step_validators_data:
                    for step_validator_data in step_validators_data:
                        TestStepValidator.objects.create(teststep=teststep, **step_validator_data)
        return testcase

    def update(self, instance, validated_data):
        teststeps_data = validated_data.pop('teststeps', False)
        # 通过testcase_id获取数据库中要进行修改的测试步骤的数据
        origin_teststeps = TestStep.objects.filter(testcase_id=instance.id)
        # 更新测试用例的数据
        instance.testcase_name = validated_data.get('testcase_name', instance.testcase_name)
        instance.testcase_desc = validated_data.get('testcase_desc', instance.testcase_desc)
        instance.testsuite = validated_data.get('testsuite', instance.testsuite)
        instance.save()
        # 删除原有的测试步骤的数据
        for origin_teststep in origin_teststeps:
            origin_teststep.delete()
        # 使用要更新的测试步骤和测试步骤校验器的数据进行新建(测试步骤和测试步骤校验器)操作
        if teststeps_data:
            for teststep_data in teststeps_data:
                step_validators_data = teststep_data.pop('step_validators', False)
                teststep = TestStep.objects.create(testcase=instance, **teststep_data)
                if step_validators_data:
                    for step_validator_data in step_validators_data:
                        TestStepValidator.objects.create(teststep=teststep, **step_validator_data)
        return instance


class RunTestCaseSerializer(BaseModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'
        read_only_fields = ('creator', 'modifier', 'testcase_name', 'testcase_desc', 'testsuite')
