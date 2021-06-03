# -*- coding: utf-8 -*-
# @Time    : 2021/4/12 下午12:48
# @Author  : anonymous
# @File    : request.py
# @Software: PyCharm
# @Description:
import json
import time
from json.decoder import JSONDecodeError

from requests import Session
from requests.utils import dict_from_cookiejar
from requests.exceptions import RequestException
from rest_framework.exceptions import ValidationError

from functions.models import Function
from testcase.models import TestStep, TestStepValidator, TestCase
from testsuite.models import TestSuite
from .parser import regx_variables, parse_request_url, regx_functions
from .response import extract_data_with_jmespath, validate_resp_data


def send_request(teststep, timeout=120):
    """
    发送接口请求并获取响应对象
    @param teststep:
    @param timeout:
    @return:
    """
    request_data = {"method": teststep.method, "url": teststep.url_path, "params": teststep.params,
                    "data": teststep.data, "headers": teststep.headers, "cookies": teststep.cookies,
                    "json": teststep.json}
    try:
        start_timestamp = time.time()
        response = Session().request(**request_data, timeout=timeout)
        # 计算一个请求的耗时(ms)
        response_time_ms = str(round((time.time() - start_timestamp) * 1000, 2)) + 'ms'
        try:
            response.json()
            return {"response_status_code": response.status_code, "response_headers": dict(response.headers),
                    "response_body": response.json(), "request_headers": dict(response.request.headers),
                    "request_url": response.url, "response_cookies": dict_from_cookiejar(response.cookies),
                    "response_encoding": response.encoding, "response_time_ms": response_time_ms
                    }
        except JSONDecodeError:
            return {"response_status_code": response.status_code, "response_headers": dict(response.headers),
                    "response_body": response.text, "request_headers": dict(response.request.headers),
                    "request_url": response.url, "response_cookies": dict_from_cookiejar(response.cookies),
                    "response_encoding": response.encoding, "response_time_ms": response_time_ms
                    }
    except RequestException as err:
        return {"RequestException": str(err)}


def handle_global_or_testcase_variables(teststep, variables):
    """
    对测试步骤中引用的全局变量(1.项目级别配置的全局变量 2.测试用例级别配置的全局变量===>来源于对测试步骤响应结果的提取)进行解析和替换
    @param teststep: 测试步骤对象
    @param variables: 全局函数 ===> dict
    @return: 直接修改测试步骤对象，无返回值
    """
    # 批量替换测试步骤中引用的全局变量
    # 对请求的url_path进行解析替换,如果没有可用全局变量,则返回原始值
    teststep.url_path = regx_variables(teststep.url_path, variables=variables)
    # 判断url_path是否符合要求
    teststep.url_path = parse_request_url(url_path=teststep.url_path)
    if teststep.json:
        if isinstance(teststep.json, str):
            teststep.json = json.loads(teststep.json)
        json_data = json.dumps(teststep.json)
        teststep.json = json.loads(regx_variables(json_data, variables=variables, is_json=True))
    if teststep.params:
        params_to_json_data = json.dumps(teststep.params)
        teststep.params = json.loads(regx_variables(params_to_json_data, variables=variables))
    if teststep.data:
        data_to_json_data = json.dumps(teststep.data)
        teststep.data = json.loads(regx_variables(data_to_json_data, variables=variables))
    if teststep.headers:
        headers_to_json_data = json.dumps(teststep.headers)
        teststep.headers = json.loads(regx_variables(headers_to_json_data, variables=variables))
    if teststep.cookies:
        cookies_to_json_data = json.dumps(teststep.cookies)
        teststep.cookies = json.loads(regx_variables(cookies_to_json_data, variables=variables))


def handle_global_functions(teststep, project_id):
    """
    对测试步骤中引用的全局函数进行解析和替换
    @param teststep: 测试步骤对象
    @param project_id: 全局函数所绑定的项目id
    @return: 直接修改测试步骤对象，无返回值
    """
    teststep.url_path = regx_functions(teststep.url_path, project_id=project_id)
    if teststep.json:
        if isinstance(teststep.json, str):
            teststep.json = json.loads(teststep.json)
        json_data = json.dumps(teststep.json)
        teststep.json = json.loads(regx_functions(json_data, project_id=project_id, is_json=True))
    if teststep.params:
        params_to_json_data = json.dumps(teststep.params)
        teststep.params = json.loads(regx_functions(params_to_json_data, project_id=project_id))
    if teststep.data:
        data_to_json_data = json.dumps(teststep.data)
        teststep.data = json.loads(regx_functions(data_to_json_data, project_id=project_id))
    if teststep.headers:
        headers_to_json_data = json.dumps(teststep.headers)
        teststep.headers = json.loads(regx_functions(headers_to_json_data, project_id=project_id))
    if teststep.cookies:
        cookies_to_json_data = json.dumps(teststep.cookies)
        teststep.cookies = json.loads(regx_functions(cookies_to_json_data, project_id=project_id))


def handle_request_data_before_send_request(teststep, config, testcase_variables):
    """
    测试步骤发起请求前，对数据进行处理
    @param testcase_variables: 
    @param teststep:
    @param config:
    @return:
    """
    # 全局函数
    testcase_id = teststep.testcase_id
    testsuite_id = TestCase.objects.get(id=testcase_id).testsuite_id
    project_id = TestSuite.objects.get(id=testsuite_id).project_id
    func_queryset_length = Function.objects.filter(project_id=project_id).count()
    if config:
        # 全局变量
        global_variables = config.global_variable
        if func_queryset_length == 1:  # 该测试步骤所在的项目下配置了全局函数
            if testcase_variables != {}:
                # 测试用例变量的优先级>全局变量：测试用例变量会覆盖全局变量(具体体现为：测试用例变量不为空时，优先于全局变量进行替换)
                handle_global_or_testcase_variables(teststep=teststep, variables=testcase_variables)
            handle_global_or_testcase_variables(teststep=teststep, variables=global_variables)
            # 对函数进行调用，并替换为函数的返回值
            handle_global_functions(teststep=teststep, project_id=project_id)

        else:
            if testcase_variables != {}:
                # 测试用例变量的优先级>全局变量：测试用例变量会覆盖全局变量(具体体现为：测试用例变量不为空时，优先于全局变量进行替换)
                handle_global_or_testcase_variables(teststep=teststep, variables=testcase_variables)
            handle_global_or_testcase_variables(teststep=teststep, variables=global_variables)
    else:
        # 未使用配置时，需要判断是否有引用了测试用例级别的变量
        if testcase_variables != {}:
            if func_queryset_length == 1:  # 该测试步骤所在的项目下配置了全局函数
                # 测试用例变量的优先级>全局变量：测试用例变量会覆盖全局变量
                handle_global_or_testcase_variables(teststep=teststep, variables=testcase_variables)
                handle_global_functions(teststep=teststep, project_id=project_id)
            else:
                # 测试用例变量的优先级>全局变量：测试用例变量会覆盖全局变量
                handle_global_or_testcase_variables(teststep=teststep, variables=testcase_variables)
    # 发送请求时：判断url_path是否符合要求
    teststep.url_path = parse_request_url(url_path=teststep.url_path)


def handle_response_data_after_send_request(teststep_resp_obj, teststep, testcase_variables):
    """
    测试步骤发起请求后，对响应对象进行处理
    @param teststep:
    @param testcase_variables:
    @param teststep_resp_obj:
    @return:
    """
    teststep_validators_results = []
    resp_obj_data = {
        "status_code": teststep_resp_obj.get('response_status_code'),
        "response_headers": teststep_resp_obj.get('response_headers'),
        "body": teststep_resp_obj.get('response_body'),
        "request_headers": teststep_resp_obj.get('request_headers'),
        "request_url": teststep_resp_obj.get('request_url'),
        "cookies": teststep_resp_obj.get('response_cookies')
    }
    # 解析提取变量的值，保存到测试用例级别的全局变量的字典testcase_variables中，该测试用例下的所有测试步骤都可以使用该字典中的全局变量
    if teststep.extract:
        for var_name, jmespath_expression in teststep.extract.items():
            extract_value = extract_data_with_jmespath(resp_obj=resp_obj_data,
                                                       jmespath_expression=jmespath_expression)
            testcase_variables[var_name] = extract_value
    # 断言处理
    teststep_validators = TestStepValidator.objects.filter(teststep_id=teststep.id)
    if len(teststep_validators) > 0:
        for teststep_validator in teststep_validators:
            res = validate_resp_data(resp_data=resp_obj_data, validator_type=teststep_validator.validator_type,
                                     jmespath_expression=teststep_validator.jmespath_expression,
                                     expected_value=teststep_validator.expected_value)
            # 断言成功/失败处理逻辑，保存断言结果到响应体对象中
            teststep_validators_results.append({'validator_id': teststep_validator.id,
                                                'validator_type': teststep_validator.validator_type,
                                                'validator_jmespath_expression': teststep_validator.jmespath_expression,
                                                'validator_expected_value': teststep_validator.expected_value,
                                                'validator_result': res
                                                })
        teststep_resp_obj['teststep_validators_results'] = teststep_validators_results
    return teststep_resp_obj


def run_teststep(teststep, config, testcase_variables):
    """
    运行测试步骤
    @param testcase_variables: 
    @param teststep:
    @param config:
    @return:
    """
    handle_request_data_before_send_request(teststep, config, testcase_variables=testcase_variables)
    teststep_resp_data = send_request(teststep=teststep)
    handle_response_data_after_send_request(teststep_resp_obj=teststep_resp_data, teststep=teststep,
                                            testcase_variables=testcase_variables)
    return teststep_resp_data


def run_testcase(testcase, config=None):
    """
    运行测试用例
    @param testcase:
    @param config:
    @return:
    """
    # testcase_variables：测试用例层面的全局变量 ===> 来源于测试步骤中的提取变量
    testcase_variables = {}
    teststeps = TestStep.objects.filter(testcase_id=testcase.id)
    testcase_resp_datas = []
    if len(teststeps) == 0:
        raise ValidationError({'Error': '测试用例的测试步骤不能为空'}, code=400)
    for teststep in teststeps:
        teststep_resp_data = run_teststep(teststep, config, testcase_variables)
        teststep_resp_data['teststep_id'] = teststep.id
        teststep_resp_data['teststep_name'] = teststep.teststep_name
        testcase_resp_datas.append(teststep_resp_data)
    return testcase_resp_datas
