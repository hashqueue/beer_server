# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 下午2:45
# @Author  : anonymous
# @File    : custom_swagger_auto_schema.py
# @Software: PyCharm
# @Description:
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'my_api_set_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags
