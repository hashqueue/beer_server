# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 下午5:29
# @Author  : anonymous
# @File    : tasks.py
# @Software: PyCharm
# @Description:
from celery import shared_task
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from testcase.models import TestCase
from config.models import Config
from utils.http_utils.request import run_testcase


@shared_task
def run_testsuite(testsuite_id, config_id=None, creator=None):
    """
    异步运行测试套件
    @param creator: 任务创建者
    @param testsuite_id:测试套件id
    @param config_id:配置项id
    @return:
    """
    config = None
    if config_id:
        config = get_object_or_404(Config, pk=config_id)
    testcases = TestCase.objects.filter(testsuite_id=testsuite_id)
    if len(testcases) == 0:
        return {'error': '运行测试套件时,测试套件中测试用例不能为空'}
    run_testsuite_result = {}
    run_testcases_result = []
    # 汇总数据
    summary_data = {'status': True, 'count': len(testcases), 'success': {'count': 0, 'testcase_ids': []},
                    'exception': {'count': 0, 'testcase_ids': []},
                    'failure': {'count': 0, 'testcase_ids': []}}
    for testcase in testcases:
        validate_flag = []
        try:
            res_data = run_testcase(testcase=testcase, config=config)
            for teststep_res_data_value in res_data:
                if teststep_res_data_value.get('teststep_validators_results', False):  # 判断是否有断言结果
                    for validate_result in teststep_res_data_value.get('teststep_validators_results'):
                        validate_flag.append(validate_result.get('validator_result').get('status'))
            if False in validate_flag:
                summary_data['failure']['count'] += 1
                summary_data['failure']['testcase_ids'].append(testcase.id)
                if summary_data['status'] is True:
                    summary_data['status'] = False
            else:
                summary_data['success']['count'] += 1
                summary_data['success']['testcase_ids'].append(testcase.id)
            run_testcases_result.append(
                {'testcase_id': testcase.id, 'testcase_name': testcase.testcase_name, "data": res_data})
        except ValidationError as err:
            if summary_data['status'] is True:
                summary_data['status'] = False
            summary_data['exception']['count'] += 1
            summary_data['exception']['testcase_ids'].append(testcase.id)
            run_testcases_result.append(
                {'testcase_id': testcase.id, 'testcase_name': testcase.testcase_name, "exception": str(err)})
    run_testsuite_result['summary_data'] = summary_data
    run_testsuite_result['run_testcases_result'] = run_testcases_result
    return run_testsuite_result
