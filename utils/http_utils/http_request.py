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


class HttpSession:
    @staticmethod
    def request(method, url, timeout=120):
        try:
            start_timestamp = time.time()
            response = Session().request(method=method, url=url, timeout=timeout)
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
    print(HttpSession.request('GET', 'https://www.baidu.com/'))
