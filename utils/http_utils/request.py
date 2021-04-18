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
import jmespath

from testcase.models import TestStep
from .parser import parse_request_url, regx_variables


def handle_request_data_before_send_request():
    pass


def handle_response_data_after_send_request():
    pass


def send_request(teststep=None, timeout=120):
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


def run_testcase(testcase, config=None):
    if config:
        # 全局变量
        global_variable = config.global_variable
        # 全局函数
        global_func = config.global_func
        teststeps = TestStep.objects.filter(testcase_id=testcase.id)
        if global_variable:
            # 批量替换测试步骤中引用的全局变量
            for teststep in teststeps:
                teststep.teststep_name = regx_variables(teststep.teststep_name, global_variables=global_variable)
                teststep.url_path = regx_variables(teststep.url_path, global_variables=global_variable)
                teststep.teststep_name = regx_variables(teststep.teststep_name, global_variables=global_variable)
                teststep.teststep_name = regx_variables(teststep.teststep_name, global_variables=global_variable)
                teststep.teststep_name = regx_variables(teststep.teststep_name, global_variables=global_variable)
                teststep.teststep_name = regx_variables(teststep.teststep_name, global_variables=global_variable)

    handle_request_data_before_send_request()
    send_request()
    handle_response_data_after_send_request()
