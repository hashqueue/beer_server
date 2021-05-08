# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 上午9:28
# @Author  : anonymous
# @File    : func_script_1.py
# @Software: PyCharm
# @Description:

import time


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    print(get_current_time())
