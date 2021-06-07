# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 下午4:34
# @Author  : anonymous
# @File    : update_global_function_content.py
# @Software: PyCharm
# @Description: Django中自定义命令文件，在每次项目线上部署时执行，用于更新根目录下global_funcs目录下所有的全局函数文件的内容

import os

from django.core.management.base import BaseCommand
from functions.models import Function
from beer_server.settings import BASE_DIR


class Command(BaseCommand):
    # 帮助文本
    help = '更新根目录下global_funcs目录下所有的全局函数文件的内容'

    # 核心业务逻辑
    def handle(self, *args, **options):
        global_func_objs_length = Function.objects.all().count()
        if global_func_objs_length > 0:
            global_func_objs = Function.objects.all()
            for obj in global_func_objs:
                # 写入全局函数内容到具体的文件中,文件名中包含了该配置绑定的project_id
                with open(os.path.join(BASE_DIR, 'global_funcs', 'func_script_project' + str(obj.project_id) + '.py'),
                          mode='w',
                          encoding='utf-8') as f:
                    f.write(obj.function_body)
            self.stdout.write('全局函数文件已经全部更新完毕!')
        else:
            self.stdout.write('暂无需要进行更新的全局函数文件!')
