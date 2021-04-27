# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 下午5:29
# @Author  : anonymous
# @File    : tasks.py
# @Software: PyCharm
# @Description:
import json
from celery import shared_task
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from testcase.models import TestCase
from config.models import Config
from utils.http_utils.request import run_testcase


@shared_task
def run_testsuite(testsuite_id, config_id=None):
    """
    异步运行测试套件
    @param testsuite_id:
    @param config_id:
    @return:
    """
    config = None
    if config_id:
        config = get_object_or_404(Config, pk=config_id)
    testcases = TestCase.objects.filter(testsuite_id=testsuite_id)
    if len(testcases) == 0:
        raise ValidationError({'Error': '测试套件的测试用例不能为空'}, code=400)
    testsuite_res_data = {}
    for testcase in testcases:
        res_data = run_testcase(testcase=testcase, config=config)
        testsuite_res_data['testcase_' + str(testcase.id)] = res_data
    return json.dumps(testsuite_res_data)
