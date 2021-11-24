# -*- coding: utf-8 -*-
# @Time    : 2021/3/14 下午10:17
# @Author  : anonymous
# @File    : custom_json_response.py
# @Software: PyCharm
# @Description:
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer


class JsonResponse(Response):
    """
    自定义接口响应数据格式类
    1.在视图类中的APIView中使用该JsonResponse返回响应数据
    2.ModelViewSet、Mixin下派生的APIView类、views.APIView都需要自己重写并返回JsonResponse格式的数据
    """

    def __init__(self, data=None, code=None, msg=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super().__init__(None, status=status)

        if isinstance(data, serializers.Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        self.data = {'code': code, 'message': msg, 'data': data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


def enveloper(serializer_class, many):
    """
    统一接口响应体格式schema
    """
    component_name = 'Enveloped{}{}'.format(
        serializer_class.__name__.replace("Serializer", ""),
        "List" if many else "",
    )

    @extend_schema_serializer(many=False, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        code = serializers.IntegerField(default=20000, read_only=True, help_text='业务状态码，20000为success；非20000为error')
        message = serializers.CharField(default='success', read_only=True, help_text='业务提示消息')
        data = serializer_class(many=many, help_text='数据')
    return EnvelopeSerializer
