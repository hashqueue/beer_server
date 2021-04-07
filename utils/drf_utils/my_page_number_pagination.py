# -*- coding: utf-8 -*-
# @Time    : 2021/3/14 下午11:04
# @Author  : anonymous
# @File    : my_page_number_pagination.py
# @Software: PyCharm
# @Description:
from rest_framework.pagination import PageNumberPagination
from .custom_json_response import JsonResponse
from rest_framework import status


class MyPageNumberPagination(PageNumberPagination):
    # 设置每页最大数据条目为50
    max_page_size = 50
    # 覆盖page_size字段为size
    page_size_query_param = 'size'
    # 配置page字段在接口文档中的描述信息
    page_query_description = '第几页'
    # 配置size字段在接口文档中的描述信息
    page_size_query_description = '每页几条'

    def get_paginated_response(self, data):
        '''
        重写父类的get_paginated_response()方法
        在分页后的数据构成的响应体中添加total_pages(总共分了多少页)和current_page_num(当前所在第几页)字段
        '''
        # 调用父类中的get_paginated_response()方法获得dict类型返回值，再进行定制
        response = super().get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current_page_num'] = self.page.number
        return JsonResponse(data=response.data, code=20000, msg='success', status=status.HTTP_200_OK)
