# -*- coding: utf-8 -*-
# @Time    : 2021/4/22 下午7:09
# @Author  : anonymous
# @File    : response.py
# @Software: PyCharm
# @Description:
import jmespath
from jmespath.exceptions import JMESPathError


def extract_data_with_jmespath(resp_obj, jmespath_expression):
    """
    从测试步骤响应对象中提取需要的数据
    @param resp_obj:
    @param jmespath_expression: jmespath表达式
    @return: jmespath表达式提取到的值
    """
    resp_obj_data = {
        "status_code": resp_obj.get('response_status_code'),
        "response_headers": resp_obj.get('response_headers'),
        "body": resp_obj.get('response_body'),
        "request_headers": resp_obj.get('request_headers'),
        "request_url": resp_obj.get('request_url'),
        "cookies": resp_obj.get('response_cookies')
    }
    try:
        extract_variable_value = jmespath.search(jmespath_expression, resp_obj_data)
        return extract_variable_value
    except JMESPathError as err:
        return {"err": str(err)}
