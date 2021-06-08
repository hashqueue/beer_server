# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 下午4:34
# @Author  : anonymous
# @File    : init_admin.py
# @Software: PyCharm
# @Description:

import os

from django.core.management.base import BaseCommand
from user.models import User
from beer_server.settings import ADMINS


class Command(BaseCommand):
    # 帮助文本
    help = '批量初始化管理员账户, 管理员账户列表可在settings.py文件同级目录下的config.ini文件中的ADMINS进行配置'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for superuser in ADMINS:
                username = superuser[0]
                email = superuser[1]
                password = 'admin.191215.*'
                self.stdout.write(f'正在创建管理员账户 <{username}> <{email}>')
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.save()
            self.stdout.write(f'批量初始化管理员账户数据完成!')
        else:
            self.stdout.write('没有可用的管理员账户数据以供初始化!')
