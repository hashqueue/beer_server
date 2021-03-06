# -*- coding: utf-8 -*-
# @Time    : 2021/4/22 下午7:09
# @Author  : anonymous
# @File    : response.py
# @Software: PyCharm
# @Description:
import jmespath
from jmespath.exceptions import JMESPathError
from rest_framework.exceptions import ValidationError


def extract_data_with_jmespath(resp_obj, jmespath_expression):
    """
    从测试步骤响应对象中提取需要的数据
    @param resp_obj: 响应体数据 dict
        {
        "status_code": http响应状态码,
        "response_headers": {...},
        "body": {...},
        "request_headers": {...},
        "request_url": http请求的url,
        "cookies": {...}
        }
    @param jmespath_expression: jmespath表达式
    @return: jmespath表达式提取到的值
    """
    try:
        extract_variable_value = jmespath.search(jmespath_expression, resp_obj)
        if extract_variable_value is None:
            jmespath_expression_list = jmespath_expression.split('.')
            keys_str = '.'.join(jmespath_expression_list[:-1])
            last_key_str = jmespath_expression_list[-1]
            # jmespath中区分未找到键的值为None 和 某个键的值就是None
            if not jmespath.search(f"contains(keys({keys_str}), '{last_key_str}')", resp_obj):
                raise ValidationError({'ValueNotFoundError': f'未找到`{jmespath_expression}`对应的值'}, code=400)
        return extract_variable_value
    except JMESPathError as err:
        raise ValidationError({'JMESPathError': str(err)}, code=400)


def validate_resp_data(resp_data, validator_type, jmespath_expression, expected_value):
    """
    测试步骤断言处理
    @param resp_data: 响应体数据 dict
        {
        "status_code": http响应状态码,
        "response_headers": {...},
        "body": {...},
        "request_headers": {...},
        "request_url": http请求的url,
        "cookies": {...}
        }
    @param validator_type: 断言类型
    @param jmespath_expression: jmespath表达式
    @param expected_value: 预期结果
    @return: 断言成功返回True，断言失败返回一个元组(False, 断言失败的原因)
    """
    try:
        actual_value = jmespath.search(jmespath_expression, resp_data)
        if actual_value is None:
            jmespath_expression_list = jmespath_expression.split('.')
            keys_str = '.'.join(jmespath_expression_list[:-1])
            last_key_str = jmespath_expression_list[-1]
            # jmespath中区分未找到键的值为None 和 某个键的值就是None
            if not jmespath.search(f"contains(keys({keys_str}), '{last_key_str}')", resp_data):
                return {'status': False, 'err': f'未找到`{jmespath_expression}`对应的值'}
    except JMESPathError as err1:
        return {'status': False, 'err': f'JMESPathError：`{str(err1)}`'}
    # 对json字符串中的true，false，null做兼容处理
    if expected_value == 'true':
        expected_value = True
    elif expected_value == 'false':
        expected_value = False
    elif expected_value == 'null':
        expected_value = None
    try:
        # equal
        if validator_type == 'equal_integer':
            assert isinstance(actual_value,
                              int), f'实际结果`{actual_value}`必须为整数(integer)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value == int(expected_value), f'实际结果`{actual_value}`不等于预期结果`{expected_value}`'

        elif validator_type == 'equal_float':
            assert isinstance(actual_value,
                              float), f'实际结果`{actual_value}`必须为小数(float)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value == float(expected_value), f'实际结果`{actual_value}`不等于预期结果`{expected_value}`'

        elif validator_type == 'equal_boolean':
            assert isinstance(actual_value,
                              bool), f'实际结果`{actual_value}`必须为布尔(boolean)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value == expected_value, f'实际结果`{actual_value}`不等于预期结果`{expected_value}`'

        elif validator_type == 'equal_null':
            assert isinstance(actual_value,
                              None.__class__), f'实际结果`{actual_value}`必须为空(null)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value == expected_value, f'实际结果`{actual_value}`不等于预期结果`{expected_value}`'

        elif validator_type == 'equal_string':
            assert isinstance(actual_value,
                              str), f'实际结果`{actual_value}`必须为字符串(string)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value == expected_value, f'实际结果`{actual_value}`不等于预期结果`{expected_value}`'

        # not equal
        elif validator_type == 'not_equal_integer':
            assert isinstance(actual_value,
                              int), f'实际结果`{actual_value}`必须为整数(integer)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value != int(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果!=预期结果`关系'

        elif validator_type == 'not_equal_float':
            assert isinstance(actual_value,
                              float), f'实际结果`{actual_value}`必须为小数(float)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value != float(
                expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果!=预期结果`关系'

        elif validator_type == 'not_equal_boolean':
            assert isinstance(actual_value,
                              bool), f'实际结果`{actual_value}`必须为布尔(boolean)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value != expected_value, f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果!=预期结果`关系'

        elif validator_type == 'not_equal_null':
            assert not isinstance(actual_value,
                                  None.__class__), f'实际结果`{actual_value}`必须为非空(非null)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value != expected_value, f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果!=预期结果`关系`'

        elif validator_type == 'not_equal_string':
            assert isinstance(actual_value,
                              str), f'实际结果`{actual_value}`必须为字符串(string)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value != expected_value, f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果!=预期结果`关系'

        # contains & contained_by
        elif validator_type == 'contained_by':
            assert str(actual_value) in expected_value, f'预期结果`{expected_value}`不包含实际结果`{actual_value}`'

        elif validator_type == 'contains':
            assert expected_value in str(actual_value), f'实际结果`{actual_value}`不包含预期结果`{expected_value}`'

        # startswith & endswith & startswith_by & endswith_by
        elif validator_type == 'startswith':
            assert str(actual_value).startswith(expected_value), f'实际结果`{actual_value}`不以预期结果`{expected_value}`开头'

        elif validator_type == 'endswith':
            assert str(actual_value).endswith(expected_value), f'实际结果`{actual_value}`不以预期结果`{expected_value}`结尾'

        elif validator_type == 'startswith_by':
            assert expected_value.startswith(str(actual_value)), f'预期结果`{expected_value}`不以实际结果`{actual_value}`开头'

        elif validator_type == 'endswith_by':
            assert expected_value.endswith(str(actual_value)), f'预期结果`{expected_value}`不以实际结果`{actual_value}`结尾'

        # greater_or_equals(大于等于)
        elif validator_type == 'greater_or_equals_integer':
            assert isinstance(actual_value,
                              int), f'实际结果`{actual_value}`必须为整数(integer)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value >= int(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果>=预期结果`关系'

        elif validator_type == 'greater_or_equals_float':
            assert isinstance(actual_value,
                              float), f'实际结果`{actual_value}`必须为小数(float)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value >= float(
                expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果>=预期结果`关系'

        # greater_than(大于)
        elif validator_type == 'greater_than_integer':
            assert isinstance(actual_value,
                              int), f'实际结果`{actual_value}`必须为整数(integer)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value > int(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果>预期结果`关系'

        elif validator_type == 'greater_than_float':
            assert isinstance(actual_value,
                              float), f'实际结果`{actual_value}`必须为小数(float)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value > float(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果>预期结果`关系'

        # less_or_equals(小于等于)
        elif validator_type == 'less_or_equals_integer':
            assert isinstance(actual_value,
                              int), f'实际结果`{actual_value}`必须为整数(integer)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value <= int(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果<=预期结果`关系'

        elif validator_type == 'less_or_equals_float':
            assert isinstance(actual_value,
                              float), f'实际结果`{actual_value}`必须为小数(float)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value <= float(
                expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果<=预期结果`关系'

        # less_than(小于)
        elif validator_type == 'less_than_integer':
            assert isinstance(actual_value,
                              int), f'实际结果`{actual_value}`必须为整数(integer)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value < int(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果<预期结果`关系'

        elif validator_type == 'less_than_float':
            assert isinstance(actual_value,
                              float), f'实际结果`{actual_value}`必须为小数(float)类型,当前实际结果数据类型为`{type(actual_value)}`'
            assert actual_value < float(expected_value), f'实际结果`{actual_value}`与预期结果`{expected_value}`不满足`实际结果<预期结果`关系'

        # 对象的length与预期结果进行比较(都是整数类型)
        elif validator_type == 'length_equal':
            assert not isinstance(actual_value, int), f'实际结果`{actual_value}`的数据类型不能为整数(integer)类型'
            assert not isinstance(actual_value, float), f'实际结果`{actual_value}`的数据类型不能为小数(float)类型'
            assert not isinstance(actual_value, None.__class__), f'实际结果`{actual_value}`的数据类型不能为空(null)类型'
            assert not isinstance(actual_value, bool), f'实际结果`{actual_value}`的数据类型不能为布尔(boolean)类型'
            assert not isinstance(actual_value, complex), f'实际结果`{actual_value}`的数据类型不能为复数(complex)类型'
            assert len(actual_value) == int(expected_value), f'实际结果的长度为`{len(actual_value)}`, 不等于预期结果`{expected_value}`'

        elif validator_type == 'length_not_equal':
            assert not isinstance(actual_value, int), f'实际结果`{actual_value}`的数据类型不能为整数(integer)类型'
            assert not isinstance(actual_value, float), f'实际结果`{actual_value}`的数据类型不能为小数(float)类型'
            assert not isinstance(actual_value, None.__class__), f'实际结果`{actual_value}`的数据类型不能为空(null)类型'
            assert not isinstance(actual_value, bool), f'实际结果`{actual_value}`的数据类型不能为布尔(boolean)类型'
            assert not isinstance(actual_value, complex), f'实际结果`{actual_value}`的数据类型不能为复数(complex)类型'
            assert len(actual_value) != int(
                expected_value), f'实际结果的长度为`{len(actual_value)}`, 预期结果为`{expected_value}`, 不满足`实际结果长度!=预期结果`关系'

        elif validator_type == 'length_greater_or_equals':
            assert not isinstance(actual_value, int), f'实际结果`{actual_value}`的数据类型不能为整数(integer)类型'
            assert not isinstance(actual_value, float), f'实际结果`{actual_value}`的数据类型不能为小数(float)类型'
            assert not isinstance(actual_value, None.__class__), f'实际结果`{actual_value}`的数据类型不能为空(null)类型'
            assert not isinstance(actual_value, bool), f'实际结果`{actual_value}`的数据类型不能为布尔(boolean)类型'
            assert not isinstance(actual_value, complex), f'实际结果`{actual_value}`的数据类型不能为复数(complex)类型'
            assert len(actual_value) >= int(expected_value), \
                f'实际结果的长度为`{len(actual_value)}`, 预期结果为`{expected_value}`, 不满足`实际结果长度>=预期结果`关系'

        elif validator_type == 'length_greater_than':
            assert not isinstance(actual_value, int), f'实际结果`{actual_value}`的数据类型不能为整数(integer)类型'
            assert not isinstance(actual_value, float), f'实际结果`{actual_value}`的数据类型不能为小数(float)类型'
            assert not isinstance(actual_value, None.__class__), f'实际结果`{actual_value}`的数据类型不能为空(null)类型'
            assert not isinstance(actual_value, bool), f'实际结果`{actual_value}`的数据类型不能为布尔(boolean)类型'
            assert not isinstance(actual_value, complex), f'实际结果`{actual_value}`的数据类型不能为复数(complex)类型'
            assert len(actual_value) > int(expected_value), \
                f'实际结果的长度为`{len(actual_value)}`, 预期结果为`{expected_value}`, 不满足`实际结果长度>预期结果`关系'

        elif validator_type == 'length_less_or_equals':
            assert not isinstance(actual_value, int), f'实际结果`{actual_value}`的数据类型不能为整数(integer)类型'
            assert not isinstance(actual_value, float), f'实际结果`{actual_value}`的数据类型不能为小数(float)类型'
            assert not isinstance(actual_value, None.__class__), f'实际结果`{actual_value}`的数据类型不能为空(null)类型'
            assert not isinstance(actual_value, bool), f'实际结果`{actual_value}`的数据类型不能为布尔(boolean)类型'
            assert not isinstance(actual_value, complex), f'实际结果`{actual_value}`的数据类型不能为复数(complex)类型'
            assert len(actual_value) <= int(expected_value), \
                f'实际结果的长度为`{len(actual_value)}`, 预期结果为`{expected_value}`, 不满足`实际结果长度<=预期结果`关系'

        elif validator_type == 'length_less_than':
            assert not isinstance(actual_value, int), f'实际结果`{actual_value}`的数据类型不能为整数(integer)类型'
            assert not isinstance(actual_value, float), f'实际结果`{actual_value}`的数据类型不能为小数(float)类型'
            assert not isinstance(actual_value, None.__class__), f'实际结果`{actual_value}`的数据类型不能为空(null)类型'
            assert not isinstance(actual_value, bool), f'实际结果`{actual_value}`的数据类型不能为布尔(boolean)类型'
            assert not isinstance(actual_value, complex), f'实际结果`{actual_value}`的数据类型不能为复数(complex)类型'
            assert len(actual_value) < int(expected_value), \
                f'实际结果的长度为`{len(actual_value)}`, 预期结果为`{expected_value}`, 不满足`实际结果长度<预期结果`关系'

        # TODO regex(正则)
        elif validator_type == 'regex_match':
            pass
        return {'status': True, 'actual_value': actual_value, 'err': None}
    except AssertionError as err2:
        return {'status': False, 'actual_value': actual_value, 'err': f'AssertionError：`{str(err2)}`'}
    except TypeError as err3:
        return {'status': False, 'actual_value': actual_value, 'err': f'TypeError(数据类型转换时发生异常)：`{str(err3)}`'}
    except Exception as err4:
        return {'status': False, 'actual_value': actual_value, 'err': f'Error：`{str(err4)}`'}


if __name__ == '__main__':
    # resp_obj_data1 = {
    #     "status_code": 200,
    #     "response_headers": {
    #         "Server": "gunicorn/19.9.0",
    #         "Date": "Sun, 25 Apr 2021 12:44:56 GMT",
    #         "Connection": "keep-alive",
    #         "Content-Type": "application/json",
    #         "Content-Length": "478",
    #         "Access-Control-Allow-Origin": "*",
    #         "Access-Control-Allow-Credentials": "true"
    #     },
    #     "body": {
    #         "code": 20000,
    #         "message": "success",
    #         "data": {
    #             "id": 1,
    #             "create_time": "2021-04-19 22:55:24",
    #             "update_time": "2021-04-19 22:55:24",
    #             "teststeps": [
    #                 {
    #                     "id": 1,
    #                     "step_validators": [],
    #                     "teststep_name": "用户登录",
    #                     "method": "POST",
    #                     "url_path": "http://anonymous.org.cn:8008/post",
    #                     "desc": "",
    #                     "json": None,
    #                     "params": None,
    #                     "data": {
    #                         "password": "admin",
    #                         "username": "admin"
    #                     },
    #                     "headers": {
    #                         "Content-Type": "application/json"
    #                     },
    #                     "cookies": None,
    #                     "export": None,
    #                     "extract": True,
    #                     "quote_testcase_id": False
    #                 }
    #             ],
    #             "creator": "admin1",
    #             "modifier": "admin1",
    #             "testcase_name": "用户登录不使用全局变量",
    #             "testcase_desc": "用户登录不使用全局变量",
    #             "testsuite": 1
    #         }
    #     },
    #     "request_headers": {
    #         "User-Agent": "python-requests/2.25.1",
    #         "Accept-Encoding": "gzip, deflate",
    #         "Accept": "*/*",
    #         "Connection": "keep-alive",
    #         "Content-Type": "application/json",
    #         "Content-Length": "52"
    #     },
    #     "request_url": "http://anonymous.org.cn:8008/post",
    #     "cookies": {}
    # }
    # print(validate_resp_data(resp_obj_data1, 'equal', 'status_code', 200))
    # print(validate_resp_data(resp_obj_data1, 'equal', 'body.data.teststeps[0].json', 'null'))
    # print(validate_resp_data(resp_obj_data1, 'equal', 'body.data.teststeps[0].extract', 'true'))
    # print(validate_resp_data(resp_obj_data1, 'equal', 'body.data.teststeps[0].quote_testcase_id', 'false'))
    # print(validate_resp_data(resp_obj_data1, 'contained_by', 'body.data.teststeps[0].method', 'GET、POST、DELETE'))
    # print(validate_resp_data(resp_obj_data1, 'contains', 'body.data.teststeps[0].url_path', 'http://anonymous.org.cn'))
    # print(validate_resp_data(resp_obj_data1, 'endswith', 'body.data.teststeps[0].url_path', 'post'))
    # print(validate_resp_data(resp_obj_data1, 'greater_or_equals', 'body.code', 120000))
    # print(validate_resp_data(resp_obj_data1, 'greater_or_equals', 'body.code', 200))
    # print(validate_resp_data(resp_obj_data1, 'greater_than', 'body.code', 200))
    # print(validate_resp_data(resp_obj_data1, 'length_equal', 'body.data.teststeps[0].teststep_name', 4))
    # print(validate_resp_data(resp_obj_data1, 'length_greater_or_equals', 'body.data.teststeps[0].teststep_name', 4))
    # print(validate_resp_data(resp_obj_data1, 'length_greater_or_equals', 'body.data.teststeps[0].teststep_name', 5))
    # print(validate_resp_data(resp_obj_data1, 'length_greater_or_equals', 'body.data.teststeps[0].teststep_name', 2))
    # print(validate_resp_data(resp_obj_data1, 'length_greater_than', 'body.data.teststeps[0].teststep_name', 2))
    # print(validate_resp_data(resp_obj_data1, 'length_less_or_equals', 'body.data.teststeps[0].teststep_name', 4))
    # print(validate_resp_data(resp_obj_data1, 'length_less_or_equals', 'body.data.teststeps[0].teststep_name', 5))
    # print(validate_resp_data(resp_obj_data1, 'length_less_or_equals', 'body.data.teststeps[0].teststep_name', 2))
    # print(validate_resp_data(resp_obj_data1, 'length_less_or_equals', 'body.data.teststeps[0].teststep_name', '1'))
    # print(validate_resp_data(resp_obj_data1, 'length_less_than', 'body.data.teststeps[0].teststep_name', 4))
    # print(validate_resp_data(resp_obj_data1, 'length_less_than', 'body.data.teststeps[0].teststep_name', 5))
    # print(validate_resp_data(resp_obj_data1, 'less_or_equals', 'body.data.teststeps[0].teststep_name', '用户登录'))
    # print(validate_resp_data(resp_obj_data1, 'less_or_equals', 'body.data.teststeps[0].id', 1))
    # print(validate_resp_data(resp_obj_data1, 'less_or_equals', 'body.data.teststeps[0].id', 2))
    # print(validate_resp_data(resp_obj_data1, 'less_than', 'body.data.teststeps[0].id', 2))
    # print(validate_resp_data(resp_obj_data1, 'less_than', 'body.data.teststeps[0].id', 1))
    # print(validate_resp_data(resp_obj_data1, 'not_equal', 'body.data.teststeps[0].id', 1))
    # print(validate_resp_data(resp_obj_data1, 'not_equal', 'body.data.teststeps[0].id', 2))
    # print(validate_resp_data(resp_obj_data1, 'not_equal', 'body.data.teststeps[0].id', 'true'))
    # print(validate_resp_data(resp_obj_data1, 'startswith', 'body.data.teststeps[0].url_path', 'post'))
    # print(validate_resp_data(resp_obj_data1, 'startswith', 'body.data.teststeps[0].url_path', 'http'))
    pass
