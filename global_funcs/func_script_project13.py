# -*- coding: utf-8 -*-
import random
import string
import time

def gen_random_string(str_len):
    """
    generate random string with specified length
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(str_len))

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def add(a, b):
    return a + b
