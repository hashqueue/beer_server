# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 下午7:54
# @Author  : anonymous
# @File    : parser.py
# @Software: PyCharm
# @Description:测试数据解析模块
import re
from rest_framework.serializers import ValidationError

# 从字符串开始位置匹配该字符串是否以`http(s)://`开头
start_with_http_pattern = r"^https?://"
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


if __name__ == '__main__':
    print(parse_request_url(base_url='http://www.baidu.com/', path='/api/v1/auth/'))
