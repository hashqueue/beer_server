# -*- coding: utf-8 -*-
import random
import string


def gen_random_string(str_len):
    """
    generate random string with specified length
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


def get_fullname(first_name, second_name):
    return first_name + second_name


def add(a, b):
    return a + b
