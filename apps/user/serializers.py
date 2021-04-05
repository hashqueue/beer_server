# -*- coding: utf-8 -*-
# @Time    : 2021/3/21 下午8:40
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CurrentUserInfoSerializer(serializers.ModelSerializer):
    """
    获取用户个人信息序列化器
    """
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, help_text='创建时间', label='创建时间')
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, help_text='更新时间', label='更新时间')

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_active',
                   'first_name', 'last_name', 'last_login', 'groups', 'user_permissions')
        read_only_fields = ('id', 'avatar', 'is_staff', 'date_joined')
        extra_kwargs = {
            'phone': {
                'min_length': 11,
                'max_length': 11,
                'error_messages': {
                    'min_length': '手机号长度必须为11位',
                    'max_length': '手机号长度必须为11位',
                },
                # 添加手机号`重复`校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此手机号已被使用')],

            },
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 150,
                'error_messages': {
                    'min_length': '用户名长度不能小于6',
                    'max_length': '用户名长度不能大于150',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'required': True,
                'allow_blank': False,
                # 添加邮箱重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已被使用')],
            },
            'department': {
                'label': '邮箱',
                'help_text': '邮箱',
                'max_length': 128,
                'error_messages': {
                    'max_length': '用户名长度不能大于128',
                }
            },
            'position': {
                'label': '职位',
                'help_text': '职位',
                'max_length': 128,
                'error_messages': {
                    'max_length': '用户名长度不能大于128',
                }
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 128,
                'error_messages': {
                    'min_length': '密码长度不能小于6',
                    'max_length': '密码长度不能大于128',
                }
            }
        }

    def validate_phone(self, value):
        """
        自定义验证器
        * 验证手机号是否合法
        """
        if re.match(r"(13\d|14[579]|15[^4\D]|17[^49\D]|18\d)\d{8}", value) is None:
            raise serializers.ValidationError('输入的手机号不合法')
        return value

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            super().update(instance, validated_data)
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        else:
            super().update(instance, validated_data)
            return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password_confirm = serializers.CharField(min_length=6,
                                             max_length=128,
                                             label='确认密码',
                                             help_text='确认密码',
                                             write_only=True,
                                             required=True,
                                             allow_blank=False,
                                             error_messages={
                                                 'min_length': '密码长度不能小于6',
                                                 'max_length': '密码长度不能大于128', })

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirm')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 150,
                'error_messages': {
                    'min_length': '用户名长度不能小于6',
                    'max_length': '用户名长度不能大于150',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'required': True,
                'allow_blank': False,
                # 添加邮箱重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已注册')],
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 128,
                'error_messages': {
                    'min_length': '密码长度不能小于6',
                    'max_length': '密码长度不能大于128',
                }
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('两次输入密码不一致')
        return attrs

    def create(self, validated_data):
        # 移除数据库模型类中不存在的字段
        validated_data.pop('password_confirm')
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def validate(self, attrs):
        """
        重写validate方法, 添加user_id字段
        :param attrs:
        :return:
        """
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return {"code": 20000, "message": "登录成功", "data": data}
