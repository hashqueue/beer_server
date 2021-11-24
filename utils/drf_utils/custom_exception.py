# -*- coding: utf-8 -*-
# @Time    : 2021/3/14 下午9:45
# @Author  : anonymous
# @File    : custom_exception.py
# @Software: PyCharm
# @Description:
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    自定义异常，需要在settings.py文件中进行全局配置
    1.在视图中的APIView中使用时,需要在验证数据的时候传入raise_exception=True说明需要使用自定义异常
    2.ModelViewSet中已经使用了raise_exception=True,所以无需配置
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        if 'detail' in response.data:
            response.data = {'code': 40000, 'message': response.data.get('detail'), 'data': None}
        else:
            response.data = {'code': 40000, 'message': response.data, 'data': None}
    return response
