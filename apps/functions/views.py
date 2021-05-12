import os

from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions

from .serializers import FunctionSerializer
from beer_server.settings import BASE_DIR
from .models import Function
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups


# Create your views here.
@extend_schema(tags=['全局函数管理'])
class FunctionsViewSet(CustomModelViewSet):
    serializer_class = FunctionSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        func_data_text = self.request.data.get('function_body')
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)
        # 写入全局函数内容到具体的文件中,文件名中包含了该配置绑定的project_id
        with open(os.path.join(BASE_DIR, 'global_funcs', 'func_script_project' + str(project_id) + '.py'), mode='w',
                  encoding='utf-8') as f:
            f.write(func_data_text)

    def perform_update(self, serializer):
        project_id = self.request.data.get('project')
        func_data_text = self.request.data.get('function_body')
        serializer.save(modifier=self.request.user.username)
        # 写入全局函数内容到具体的文件中,文件名中包含了该配置绑定的project_id
        with open(os.path.join(BASE_DIR, 'global_funcs', 'func_script_project' + str(project_id) + '.py'), mode='w',
                  encoding='utf-8') as f:
            f.write(func_data_text)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Function.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = Function.objects.filter(
                Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset
