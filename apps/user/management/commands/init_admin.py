# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 下午4:34
# @Author  : anonymous
# @File    : init_admin.py
# @Software: PyCharm
# @Description:

import os

from django.core.management.base import BaseCommand
from user.models import User
from beer_server.settings import ADMINS, config


class Command(BaseCommand):
    # 帮助文本
    help = '批量初始化管理员账户, 管理员账户列表可在compose/server目录下的config.ini文件中的ADMINS进行配置'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for superuser in ADMINS:
                username = superuser[0]
                email = superuser[1]
                password = config.get_string_value('email', 'ADMINS_PASSWORD')
                self.stdout.write(f'Creating administrator account <{username}> <{email}>  🌿 🌿 🌿')
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.save()
            self.stdout.write(f'Initializing the administrator account is complete. ✅')
        else:
            self.stdout.write('There is no admin account data available for initialization.  🌿 🌿 🌿')
