import os

from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .serializers import FunctionSerializer
from beer_server.settings import BASE_DIR
from .models import Function
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['全局函数管理'])
class FunctionsViewSet(ModelViewSet):
    serializer_class = FunctionSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]
    filterset_fields = ['function_name', 'function_desc', 'creator', 'modifier', 'project']

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        func_data_text = self.request.data.get('function_body')
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)
        # 写入全局函数内容到具体的文件中,文件名中包含了该函数绑定的project_id
        with open(os.path.join(BASE_DIR, 'global_funcs', 'func_script_project' + str(project_id) + '.py'), mode='w',
                  encoding='utf-8') as f:
            f.write(func_data_text)

    def perform_update(self, serializer):
        project_id = self.request.data.get('project')
        func_data_text = self.request.data.get('function_body')
        serializer.save(modifier=self.request.user.username)
        # 写入全局函数内容到具体的文件中,文件名中包含了该函数绑定的project_id
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

    @extend_schema(responses=enveloper(FunctionSerializer, False))
    def create(self, request, *args, **kwargs):
        """
        新增函数
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    @extend_schema(responses=enveloper(FunctionSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取函数列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/functions/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "function_name": "string",
                "function_desc": "string",
                "function_body": "string",
                "project": 0
              },
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "function_name": "string",
                "function_desc": "string",
                "function_body": "string",
                "project": 0
              },
            ],
            "total_pages": 16,
            "current_page": 1
          }
        }
        ```
        """
        res = super().list(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(FunctionSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看函数详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(FunctionSerializer, False))
    def update(self, request, *args, **kwargs):
        """
        更新函数
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(FunctionSerializer, False))
    def partial_update(self, request, *args, **kwargs):
        """
        更新函数
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除函数
        """
        return super().destroy(request, *args, **kwargs)
