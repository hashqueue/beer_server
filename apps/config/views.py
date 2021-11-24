from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .serializers import ConfigSerializer
from .models import Config
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['配置管理'])
class ConfigsViewSet(ModelViewSet):
    serializer_class = ConfigSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]
    filterset_fields = ['config_name', 'config_desc', 'creator', 'modifier', 'project']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Config.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = Config.objects.filter(Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset

    @extend_schema(responses=enveloper(ConfigSerializer, False))
    def create(self, request, *args, **kwargs):
        """
        新增配置
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    @extend_schema(responses=enveloper(ConfigSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取配置列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/configs/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "config_name": "string",
                "config_desc": "string",
                "global_variable": {
                "property1": null,
                "property2": null
                },
                "project": 0
              },
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "config_name": "string",
                "config_desc": "string",
                "global_variable": {
                "property1": null,
                "property2": null
                },
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

    @extend_schema(responses=enveloper(ConfigSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看配置详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(ConfigSerializer, False))
    def update(self, request, *args, **kwargs):
        """
        更新配置
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(ConfigSerializer, False))
    def partial_update(self, request, *args, **kwargs):
        """
        更新配置
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除配置
        """
        return super().destroy(request, *args, **kwargs)
    