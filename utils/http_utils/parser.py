# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 下午7:54
# @Author  : anonymous
# @File    : parser.py
# @Software: PyCharm
# @Description:测试数据解析模块
import ast
import re
import importlib
from types import FunctionType
from typing import Dict, Any

from rest_framework.serializers import ValidationError

# 从字符串开始位置匹配该字符串是否以`http(s)://`开头
from typing_extensions import Text

start_with_http_pattern = r"^http(s)?://"
# 从字符串开始位置匹配该字符串是否`不`以`//`结尾
not_end_with_double_slash_pattern = r'.*(?<!//)$'


def parse_string_value(str_value: Text) -> Any:
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


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


def regx_variables(raw_text: Any, variables: dict) -> str:
    """
    对请求数据中引用了全局变量或测试用例变量的数据进行解析，然后替换为全局变量或测试用例变量中变量的具体的值
    @param variables: 可选的全局变量或测试用例变量
    @param raw_text: 请求数据中需要进行解析替换为全局变量或测试用例变量值的数据
    @return: 已完成替换的请求数据
    """
    need_replace_vars_list = re.findall(r'\$(\w+)', raw_text)
    for raw_variable in need_replace_vars_list:
        for key in variables.keys():
            if key in raw_variable:
                raw_variable = key
        try:
            if isinstance(variables[raw_variable], str):
                raw_text = re.sub(r'\$' + raw_variable, variables[raw_variable], raw_text)
            else:
                raw_text = variables[raw_variable]
        except KeyError as err:
            raise ValidationError({raw_text: f"未在项目配置中找到{raw_variable}变量, err_detail:{err}"}, code=400)
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
    imported = importlib.import_module('global_funcs.func_script_' + str(project_id))
    functions_data = {}
    for item in list(filter(is_function, vars(imported).items())):
        functions_data[item[0]] = item[1]
    return functions_data


def parse_function_params(params: Text, variables: Dict) -> Dict:
    """
    parse function params to args and kwargs.
    @param variables: 项目级别的全局变量或测试用例级别的全局变量
    @param params: function param in string
    @return: dict: function meta dict

            {
                "args": [],
                "kwargs": {}
            }
    >>> global_vars11 = {'base_url': 'www.baidu.com', 'url_path': 'api/v1/auth/projects/', 'username': 'admin1',
        'password': '111111'}
    >>> parse_function_params(params='1, "2", http://$base_url/api/v1/, name=$username, age=$age, pass="111111", del=True', variables=global_vars)
    >>> {'args': [1, '2', 'http://www.baidu.com/api/v1/'], 'kwargs': {'age': 21, 'name': 'admin1', 'pass': '111111', 'del': True}}
    """
    function_meta = {"args": [], "kwargs": {}}

    params_str = params.strip()
    if params_str == "":
        return function_meta

    args_list = params_str.split(",")
    for arg in args_list:
        arg = arg.strip()
        if "=" in arg:
            key, value = arg.split("=")
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
            # 如果函数的关键字参数里有字符串的话，判断以下该字符串使用引用了全局变量，有就替换
            if isinstance(function_meta["kwargs"][key.strip()], str):
                function_meta["kwargs"][key.strip()] = regx_variables(raw_text=function_meta["kwargs"][key.strip()],
                                                                      variables=variables)
        else:
            function_meta["args"].append(parse_string_value(arg.strip()))
    # 如果函数的位置参数里有字符串的话，判断以下该字符串使用引用了全局变量，有就替换
    for index in range(len(function_meta["args"])):
        if isinstance(function_meta["args"][index], str):
            function_meta["args"][index] = regx_variables(raw_text=function_meta["args"][index],
                                                          variables=variables)
    return function_meta


def regx_functions(content: str):
    """
    extract all functions from string content, which are in format ${fun()}
    @param content:
    @return:
    """
    need_execute_raw_funcs_list = re.findall(r"\${(\w+)\(([$\w.\-/\s=,]*)\)}", content)
    return need_execute_raw_funcs_list


if __name__ == '__main__':
    # print(parse_request_url(url_path='https://www.baidu.com/api/v1/auth/'))
    # url = "http://$1base_url.cn/sys/$url_path/model/"
    # url = "http://base_url.cn/sys/url_path/model/"
    global_vars = {'base_url': 'www.baidu.com', 'url_path': 'api/v1/auth/projects/', 'username': 'admin1',
                   'password': '111111', 'age': {"q": 1}}
    # url = regx_variables(raw_text=url, variables=global_vars)
    # print(url)
    # print(get_func_mapping(1))
    # print(regx_functions("""/api/${add(1, 2, name=$admin)}p/"""))
    print(parse_function_params(params="""1, 3.1415926, "2", http://$base_url/api/v1/, qqq={'q': 'a', 'count': 1}, age=$age, name=$username, pass="111111", del=True""",
                                variables=global_vars))
