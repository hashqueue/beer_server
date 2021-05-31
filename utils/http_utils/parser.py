# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 下午7:54
# @Author  : anonymous
# @File    : parser.py
# @Software: PyCharm
# @Description: 测试数据解析模块
import json
import re
import importlib
from types import FunctionType
from typing import Any

from rest_framework.serializers import ValidationError

# 从字符串开始位置匹配该字符串是否以`http(s)://`开头
start_with_http_pattern = r"^http(s)?://"
# 从字符串开始位置匹配该字符串是否`不`以`//`结尾
not_end_with_double_slash_pattern = r'.*(?<!//)$'


def parse_request_url(url_path: str = None) -> str:
    """
    解析请求中的url
    @param url_path: 请求的url_path,可以使绝对路径(https://www.baidu.com/help/)，也可以是相对路径(/help/)
    @return:
    """
    if re.match(start_with_http_pattern, url_path):
        if re.match(not_end_with_double_slash_pattern, url_path):
            return url_path
        else:
            raise ValidationError({url_path: "请求的base_url不能以`//`结尾,必须设置域名或ip:port"}, code=400)
    else:
        raise ValidationError({url_path: "测试步骤中的url_path未以`http(s)://`开头"}, code=400)


def regx_variables(raw_text: str, variables: dict, is_json: bool = False) -> Any:
    """
    对请求数据中引用了全局变量或测试用例变量的数据进行解析，然后替换为全局变量或测试用例变量中变量的具体的值
    @param is_json:
    @param variables: 可选的全局变量或测试用例变量
    @param raw_text: 请求数据中需要进行解析替换为全局变量或测试用例变量值的数据
    @return: 已完成替换的请求数据
    """
    need_replace_vars_list = re.findall(r'\$(\w+)', raw_text)
    print(need_replace_vars_list)
    for raw_variable in need_replace_vars_list:
        for key in variables.keys():
            if key in raw_variable:
                raw_variable = key
        try:
            # 如果json格式请求参数中引用了全局函数，需要判断具体参数的类型("12" ===> 12)，form-data和params在server端接收时会自动将"12"转换为12
            if is_json:
                if isinstance(variables[raw_variable], bool):
                    # 如果全局变量/测试用例变量的某个key的值为布尔类型
                    if variables[raw_variable]:
                        raw_text = raw_text.replace('"$' + raw_variable + '"', 'true')
                    else:
                        raw_text = raw_text.replace('"$' + raw_variable + '"', 'false')
                elif isinstance(variables[raw_variable], None.__class__):
                    # 如果全局变量/测试用例变量的某个key的值为None类型
                    raw_text = raw_text.replace('"$' + raw_variable + '"', 'null')
                elif isinstance(variables[raw_variable], int) or isinstance(variables[raw_variable], float):
                    # 如果全局变量/测试用例变量的某个key的值为int或float类型
                    print(type(variables[raw_variable]))
                    raw_text = raw_text.replace('"$' + raw_variable + '"', str(variables[raw_variable]))
                else:
                    # 如果全局变量/测试用例变量的某个key的值为字符串类型
                    raw_text = re.sub(r'\$' + raw_variable, str(variables[raw_variable]), raw_text)
            else:
                raw_text = re.sub(r'\$' + raw_variable, str(variables[raw_variable]), raw_text)
        except KeyError as err:
            raise ValidationError({raw_text: f"未找到{raw_variable}变量, err_detail: {err}"}, code=400)
    return raw_text


def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function.
    """
    func_name, func_obj = tup
    return isinstance(func_obj, FunctionType)


def get_func_mapping(project_id):
    """
    获取项目绑定的全局函数模块内的所有函数映射
    @param project_id: 项目id
    @return: dict ===> {"func_name": function obj}
    """
    imported = importlib.import_module('global_funcs.func_script_project' + str(project_id))
    functions_data = {}
    for item in list(filter(is_function, vars(imported).items())):
        functions_data[item[0]] = item[1]
    return functions_data


def regx_functions(content: str, project_id: int = None, is_json: bool = False) -> Any:
    """
    从字符串内容中提取所有函数，其格式为${func_name(param1, param2, key1=value1)}
    执行函数并获得返回值，并在content中进行替换为函数的执行后的返回值
    @param is_json:
    @param project_id:
    @param content:
    @return:
    .strip('${').strip('}')
    """
    need_execute_raw_funcs_list = re.findall(r"\${(\w+\([^)]*\))}", content)
    for raw_func in need_execute_raw_funcs_list:
        data = {}
        code = 'from global_funcs.func_script_project' + str(
            project_id) + ' import *\ncode_execute_result = ' + raw_func
        try:
            exec(code, data)
            # 如果json格式请求参数中引用了全局函数，需要判断具体参数的类型("12" ===> 12)，form-data和params在server端接收时会自动将"12"转换为12
            if is_json:
                if isinstance(data['code_execute_result'], bool):
                    if data['code_execute_result']:
                        content = content.replace('"${' + raw_func + '}"', 'true')
                    else:
                        content = content.replace('"${' + raw_func + '}"', 'false')
                elif isinstance(data['code_execute_result'], None.__class__):
                    content = content.replace('"${' + raw_func + '}"', 'null')
                elif isinstance(data['code_execute_result'], int) or isinstance(data['code_execute_result'], float):
                    content = content.replace('"${' + raw_func + '}"', str(data['code_execute_result']))
                else:
                    content = content.replace('${' + raw_func + '}', str(data['code_execute_result']))
            else:
                content = content.replace('${' + raw_func + '}', str(data['code_execute_result']))
        except Exception as err:
            raise ValidationError({'函数执行时异常': f"出现异常的函数为{raw_func}, err_detail: {err}"}, code=400)
    return content


if __name__ == '__main__':
    # print(parse_request_url(url_path='https://www.baidu.com/api/v1/auth/'))
    # url = "http://$1base_url.cn/sys/$url_path/model/"
    # url = json.dumps({"url": "http://$base_url.cn/sys/$url_path/model/", "age": "${add_str(3.13, 5.37)}哈哈哈"})
    # global_vars = {'base_url': 'www.baidu.com', 'url_path': 'api/v1/auth/projects/', 'username': 'admin1',
    #                'password': '111111', 'q': 12}
    # url = regx_variables(raw_text=url, variables=global_vars, is_json=True)
    # print(url)
    # print(json.loads(url))
    # print(type(json.loads(url)))
    # print(get_func_mapping(1))
    # print(json.loads(regx_functions(url, project_id=1, is_json=True)))
    # print(type(json.loads(regx_functions(url, project_id=1, is_json=True))))
    pass