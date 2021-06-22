# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 上午9:10
# @Author  : anonymous
# @File    : custom_permissions.py
# @Software: PyCharm
# @Description:

from rest_framework import permissions


class IsObjectCreatorOrModifierInRequestUserGroups(permissions.BasePermission):
    """
    自定义对象权限类
    """
    def has_object_permission(self, request, view, obj):
        """
        判断对象的
        @param request:
        @param view:
        @param obj:
        @return:
        """
        # 演示环境禁止删除数据
        if request.method == 'DELETE':
            return False
        users_list = []
        current_login_user_groups = request.user.groups.all()
        for group_obj in current_login_user_groups:
            for user_obj in group_obj.user_set.all():
                users_list.append(user_obj.username)
        # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
        users_set = list(set(users_list))
        # 如果是superuser则可以访问所有数据；
        # 如果不是superuser，则需要判断当前数据对象的创建者和修改者 是否在 当前登录用户所在的用户组下 的 所有用户列表中
        # 主要是为了以用户组为级别来进行权限控制
        if (obj.creator in users_set and obj.modifier in users_set) or request.user.is_superuser is True:
            return True
        else:
            return False
