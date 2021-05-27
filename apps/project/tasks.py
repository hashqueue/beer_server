# -*- coding: utf-8 -*-
# @Time    : 2021/4/29 下午4:30
# @Author  : anonymous
# @File    : tasks.py
# @Software: PyCharm
# @Description:

from celery import shared_task
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from testcase.models import TestCase
from testsuite.models import TestSuite
from config.models import Config
from utils.http_utils.request import run_testcase


@shared_task
def run_project(project_id, config_id=None, creator=None):
    """
    异步运行项目
    @param project_id: 项目id
    @param creator: 任务创建者
    @param config_id:配置项id
    @return:
    """
    config = None
    if config_id:
        config = get_object_or_404(Config, pk=config_id)
    testsuites = TestSuite.objects.filter(project_id=project_id)
    if len(testsuites) == 0:
        return {'error': '运行项目时,项目中的测试套件不能为空'}
    testcases_all = []
    for testsuite in testsuites:
        testcases = TestCase.objects.filter(testsuite_id=testsuite.id)
        print(repr(testcases))
        print(testsuite.id)
        if len(testcases) == 0:
            # TODO 此处return欠妥，e.g. 某个项目下有3个套件，两个套件下用例不为空，另外一个套件下用例为空。
            #  此处为for循环，如果拿到用例为空会直接return，忽略了其他两个有用例的套件
            return {'error': '运行项目时,项目中的测试套件中的测试用例不能为空'}
        testcases_all.extend(testcases)
    run_project_result = {}
    run_testsuites_result = []
    # 项目级别的汇总数据
    summary_data = {'status': True,
                    'testsuite_info': {'testsuite_count': len(testsuites), 'testsuite_ids': []},
                    'testcase_info': {
                        'testcase_count': len(testcases_all),
                        'success': {'count': 0, 'testcase_ids': []},
                        'exception': {'count': 0, 'testcase_ids': []},
                        'failure': {'count': 0, 'testcase_ids': []}
                    }
                    }
    for testsuite in testsuites:
        summary_data['testsuite_info']['testsuite_ids'].append(testsuite.id)
        run_testsuite_result = {}
        run_testcases_result = []
        testcases = TestCase.objects.filter(testsuite_id=testsuite.id)
        # 测试套件级别的汇总数据
        testsuite_summary_data = {'creator': creator, 'count': len(testcases),
                                  'success': {'count': 0, 'testcase_ids': []},
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
                    # 项目层面计算测试用例的成功/失败/异常的比例
                    summary_data['testcase_info']['failure']['count'] += 1
                    summary_data['testcase_info']['failure']['testcase_ids'].append(testcase.id)
                    if summary_data['status'] is True:
                        summary_data['status'] = False
                    # 测试套件层面计算测试用例的成功/失败/异常的比例
                    testsuite_summary_data['failure']['count'] += 1
                    testsuite_summary_data['failure']['testcase_ids'].append(testcase.id)
                else:
                    summary_data['testcase_info']['success']['count'] += 1
                    summary_data['testcase_info']['success']['testcase_ids'].append(testcase.id)
                    testsuite_summary_data['success']['count'] += 1
                    testsuite_summary_data['success']['testcase_ids'].append(testcase.id)
                run_testcases_result.append({'testcase_id': testcase.id, 'data': res_data})
            except ValidationError as err:
                if summary_data['status'] is True:
                    summary_data['status'] = False
                summary_data['testcase_info']['exception']['count'] += 1
                summary_data['testcase_info']['exception']['testcase_ids'].append(testcase.id)
                testsuite_summary_data['exception']['count'] += 1
                testsuite_summary_data['exception']['testcase_ids'].append(testcase.id)
                run_testcases_result.append({'testcase_id': testcase.id, 'exception': str(err)})
        run_testsuite_result['summary_data'] = testsuite_summary_data
        run_testsuite_result['run_testcases_result'] = run_testcases_result
        run_testsuite_result['testsuite_id'] = testsuite.id
        run_testsuites_result.append(run_testsuite_result)
    run_project_result['summary_data'] = summary_data
    run_project_result['run_testsuites_result'] = run_testsuites_result
    return run_project_result
