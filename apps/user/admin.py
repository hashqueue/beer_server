from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserAdmin(UserAdmin):
    """
    自定义admin后台
    添加一些UserAdmin中没有设置的字段
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'department', 'position', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'department', 'position', 'is_staff', 'is_superuser',
                    'phone', 'date_joined', 'update_time')
    search_fields = ('username', 'email', 'department', 'position', 'is_staff', 'phone')
    ordering = ('username', 'date_joined')


# Register your models here.
admin.site.register(User, MyUserAdmin)
