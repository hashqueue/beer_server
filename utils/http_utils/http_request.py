# -*- coding: utf-8 -*-
# @Time    : 2021/4/12 下午12:48
# @Author  : anonymous
# @File    : http_request.py
# @Software: PyCharm
# @Description:
import time
from json.decoder import JSONDecodeError

from requests import Session
from requests.exceptions import RequestException
from testcase.models import TestCase
from testsuite.models import TestSuite
from project.models import Project


def parse_global_params(teststep, origin_global_param):
    testcase = TestCase.objects.get(id=teststep.testcase_id)
    testsuite = TestSuite.objects.get(id=testcase.testsuite_id)
    project = Project.objects.get(id=testsuite.project_id)
    project_global_params = project.config_set.all()
    for project_global_param in project_global_params:
        pass


def handle_data(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res

    return wrapper


@handle_data
def send_request(teststep, timeout=120):
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


if __name__ == '__main__':
    # print(HttpSession.request('GET', 'https://www.baidu.com/'))
    pass
