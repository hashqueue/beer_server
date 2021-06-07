# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 上午9:03
# @Author  : anonymous
# @File    : handle_config.py
# @Software: PyCharm
# @Description: 配置文件读取类

from configparser import ConfigParser


class HandleConfig:
    def __init__(self, file_name):
        """
        初始化方法,用作创建HandleConfig类的实例时创建配置文件路径实例变量,并创建配置解析器对象去指定读取的配置文件路径
        :param file_name:
        """
        # 创建HandleConfig类的实例时需要传入配置文件的文件路径然后赋值给实例变量self.file_name
        self.file_name = file_name
        # 创建配置解析器对象
        self.config = ConfigParser()
        # 去指定读取的配置文件路径
        self.config.read(self.file_name, encoding='utf-8')

    def get_string_value(self, section, option):
        """
        根据区域名和选项名返回str类型配置数据值
        :param section:区域名
        :param option: 选项名
        :return:
        """
        return self.config.get(section, option)

    def get_int_value(self, section, option):
        """
        根据区域名和选项名返回int类型配置数据值
        :param section:区域名
        :param option: 选项名
        :return:
        """
        return self.config.getint(section, option)

    def get_float_value(self, section, option):
        """
        根据区域名和选项名返回float类型配置数据值
        :param section:区域名
        :param option:选项名
        :return:
        """
        return self.config.getfloat(section, option)

    def get_boolean_value(self, section, option):
        """
        根据区域名和选项名返回bool类型配置数据值
        :param section: 区域名
        :param option: 选项名
        :return:
        """
        return self.config.getboolean(section, option)
