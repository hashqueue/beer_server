import os
from drf_spectacular.utils import extend_schema
from rest_framework import permissions

from .serializers import FunctionSerializer
from beer_server.settings import BASE_DIR
from .models import Function
from utils.drf_utils.custom_model_view_set import CustomModelViewSet


# Create your views here.
@extend_schema(tags=['全局函数管理'])
class FunctionsViewSet(CustomModelViewSet):
    queryset = Function.objects.all().order_by('-id')
    serializer_class = FunctionSerializer
    permission_classes = [permissions.IsAuthenticated]

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
