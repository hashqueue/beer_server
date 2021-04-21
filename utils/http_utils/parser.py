# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 下午7:54
# @Author  : anonymous
# @File    : parser.py
# @Software: PyCharm
# @Description:测试数据解析模块
import re
from rest_framework.serializers import ValidationError

# 从字符串开始位置匹配该字符串是否以`http(s)://`开头
start_with_http_pattern = r"^http(s)?://"
# 从字符串开始位置匹配该字符串是否`不`以`//`结尾
not_end_with_double_slash_pattern = r'.*(?<!//)$'


def parse_request_url(base_url: str = None, path: str = None) -> str:
    """
    解析请求中的url
    @param base_url:如果项目配置中的全局变量中设置了base_url,就与path进行拼接
    @param path: 请求的url_path,可以使绝对路径(https://www.baidu.com/help/)，也可以是相对路径(/help/)
    @return: 完整的url：https://www.baidu.com/help/
    """
    if re.match(start_with_http_pattern, path):
        return path
    elif base_url:
        if re.match(start_with_http_pattern, base_url):
            if re.match(not_end_with_double_slash_pattern, base_url):
                return "{}/{}".format(base_url.rstrip("/"), path.lstrip("/"))
            else:
                raise ValidationError("请求的base_url不能以`//`结尾,必须设置域名或ip:port")
        else:
            raise ValidationError("请求的base_url未以`http(s)://`开头")
    else:
        raise ValidationError("测试步骤中的url_path未以`http(s)://`开头")


def regx_variables(raw_text: str, global_variables: dict) -> str:
    """
    对请求数据中引用了全局变量的数据进行解析，然后替换为全局变量中变量的具体的值
    @param raw_text: 请求数据中需要进行解析替换为全局变量值的数据
    @param global_variables: 可选的全局变量
    @return: 已完成替换的请求数据
    """
    need_replace_vars_list = re.findall(r'\$(\w+)', raw_text)
    for raw_variable in need_replace_vars_list:
        for key in global_variables.keys():
            if key in raw_variable:
                raw_variable = key
        try:
            raw_text = re.sub(r'\$' + raw_variable, global_variables[raw_variable], raw_text)
        except KeyError as err:
            raise ValidationError(f"未在项目配置中找到{raw_variable}全局变量")
    return raw_text


if __name__ == '__main__':
    # print(parse_request_url(base_url='http://www.baidu.com/', path='/api/v1/auth/'))
    url = "http://$base_url.cn/sys/$url_path/model/"
    global_vars = {'base_url': 'www.baidu.com', 'url_path': 'api/v1/auth/projects/', 'username': 'admin1',
                   'password': '111111'}
    url = regx_variables(raw_text=url, global_variables=global_vars)
    print(url)
