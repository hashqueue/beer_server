# -*- coding: utf-8 -*-
# @Time    : 2021/3/14 下午9:45
# @Author  : anonymous
# @File    : custom_exception.py
# @Software: PyCharm
# @Description:
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    """
    自定义异常，需要在settings.py文件中进行全局配置
    1.在视图中的APIView中使用时,需要在验证数据的时候传入raise_exception=True说明需要使用自定义异常
    2.ModelViewSet中已经使用了raise_exception=True,所以无需配置
    """
    response = exception_handler(exc, context)
    # 对具体报错做兼容
    if isinstance(exc, ValidationError):
        response.data['code'] = 40000
        response.data['data'] = []
        if isinstance(response.data, dict):
            data_new = dict(response.data)
            data_new.pop('code')
            data_new.pop('data')
            response.data['message'] = data_new
            for key in dict(response.data).keys():
                if key not in ['code', 'data', 'message']:
                    response.data.pop(key)
        else:
            response.data['message'] = '输入有误'
        return response
    if response is not None:
        if response.status_code == 401:
            err_msg = response.data.pop('detail')
            response.data.clear()
            response.data['message'] = err_msg
            response.data['code'] = 40001
            response.data['data'] = []
            return response
        response.data.clear()
        response.data['data'] = []
        if response.status_code == 400:
            response.data['message'] = '输入有误'
            response.data['code'] = 40000
        elif response.status_code == 403:
            response.data['message'] = '没有权限执行该操作'
            response.data['code'] = 40003
        elif response.status_code == 404:
            response.data['message'] = '未找到资源'
            response.data['code'] = 40004
        elif response.status_code == 405:
            response.data['message'] = '请求方法不允许'
            response.data['code'] = 40005
        elif response.status_code == 406:
            response.data['message'] = '无法满足请求Accept标头'
            response.data['code'] = 40006
        elif response.status_code == 415:
            response.data['message'] = '请求中有不支持的媒体类型'
            response.data['code'] = 40015
        elif response.status_code == 429:
            response.data['message'] = '请求被限制'
            response.data['code'] = 40029
        elif response.status_code == 500:
            response.data['message'] = '服务器内部错误'
            response.data['code'] = 50000
        else:
            response.data['message'] = '未知错误'
        return response
    return response
