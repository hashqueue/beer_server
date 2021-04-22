# -*- coding: utf-8 -*-
# @Time    : 2021/4/12 下午12:48
# @Author  : anonymous
# @File    : request.py
# @Software: PyCharm
# @Description:
import time
from json.decoder import JSONDecodeError

from requests import Session
from requests.exceptions import RequestException

from testcase.models import TestStep
from .parser import regx_variables, parse_request_url
from .response import extract_data_with_jmespath


def handle_global_and_testcase_variables(teststep, variables):
    # 批量替换测试步骤中引用的全局变量
    # 对请求的url_path进行解析替换,如果没有可用全局变量,则返回原始值
    teststep.url_path = regx_variables(teststep.url_path, variables=variables)
    # 判断url_path是否符合有要求
    teststep.url_path = parse_request_url(url_path=teststep.url_path)
    if teststep.params:
        for params_item in teststep.params.keys():
            teststep.params[params_item] = regx_variables(teststep.params[params_item], variables=variables)
    if teststep.data:
        for data_item in teststep.data.keys():
            teststep.data[data_item] = regx_variables(teststep.data[data_item], variables=variables)
    if teststep.headers:
        for headers_item in teststep.headers.keys():
            teststep.headers[headers_item] = regx_variables(teststep.headers[headers_item], variables=variables)
    if teststep.cookies:
        for cookies_item in teststep.cookies.keys():
            teststep.cookies[cookies_item] = regx_variables(teststep.cookies[cookies_item], variables=variables)


def handle_request_data_before_send_request(teststep, config, testcase_variables):
    """
    测试步骤发起请求前，对数据进行处理
    @param testcase_variables: 
    @param teststep:
    @param config:
    @return:
    """
    if config:
        # 全局变量
        global_variables = config.global_variable
        # 全局函数
        global_func = config.global_func
        handle_global_and_testcase_variables(teststep=teststep, variables=global_variables)
    if testcase_variables != {}:
        # 测试用例变量的优先级>全局变量：测试用例变量会覆盖全局变量
        handle_global_and_testcase_variables(teststep=teststep, variables=testcase_variables)
    # 发送请求时：判断url_path是否符合要求
    teststep.url_path = parse_request_url(url_path=teststep.url_path)
    return teststep


def handle_response_data_after_send_request(teststep_resp_obj, teststep_extract, testcase_variables):
    """
    测试步骤发起请求后，对响应对象进行处理
    @param testcase_variables: 
    @param teststep_extract: 
    @param teststep_resp_obj:
    @return:
    """
    if teststep_extract:
        for var_name, jmespath_expression in teststep_extract.items():
            resp = extract_data_with_jmespath(resp_obj=teststep_resp_obj, jmespath_expression=jmespath_expression)
            testcase_variables['$' + var_name] = resp
    return teststep_resp_obj


def send_request(teststep=None, timeout=120):
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
        response_time_ms = round((time.time() - start_timestamp) * 1000, 2)
        try:
            response.json()
            return {"response_status_code": response.status_code, "response_headers": response.headers,
                    "response_body": response.json(), "request_headers": response.request.headers,
                    "request_url": response.url, "response_cookies": response.cookies,
                    "response_encoding": response.encoding, "response_time_ms": response_time_ms
                    }
        except JSONDecodeError:
            return {"response_status_code": response.status_code, "response_headers": response.headers,
                    "response_body": response.text, "request_headers": response.request.headers,
                    "request_url": response.url, "response_cookies": response.cookies,
                    "response_encoding": response.encoding, "response_time_ms": response_time_ms
                    }
    except RequestException as err:
        return {"err": str(err)}


def run_teststep(teststep, config, testcase_variables):
    """
    运行测试步骤
    @param testcase_variables: 
    @param teststep:
    @param config:
    @return:
    """
    teststep_new = handle_request_data_before_send_request(teststep, config, testcase_variables=testcase_variables)
    teststep_resp_data = send_request(teststep=teststep_new)
    handle_response_data_after_send_request(teststep_resp_obj=teststep_resp_data, teststep_extract=teststep.extract,
                                            testcase_variables=testcase_variables)
    return teststep_resp_data


def run_testcase(testcase, config=None):
    """
    运行测试用例
    @param testcase:
    @param config:
    @return:
    """
    # 测试用例层面的全局变量 ===> 来源于测试步骤中的提取变量
    testcase_variables = {}
    teststeps = TestStep.objects.filter(testcase_id=testcase.id)
    testcase_resp_datas = {}
    for teststep in teststeps:
        teststep_resp_data = run_teststep(teststep, config, testcase_variables)
        testcase_resp_datas[teststep.teststep_name] = teststep_resp_data
    return testcase_resp_datas
