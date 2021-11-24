from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .serializers import GroupSerializer
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['用户组管理'])
class GroupsViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=enveloper(GroupSerializer, False))
    def create(self, request, *args, **kwargs):
        """
        新增用户组
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    @extend_schema(responses=enveloper(GroupSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取用户组列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/groups/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "name": "string"
              },
              {
                "id": 0,
                "name": "string"
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

    @extend_schema(responses=enveloper(GroupSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看用户组详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(GroupSerializer, False))
    def update(self, request, *args, **kwargs):
        """
        更新用户组
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(GroupSerializer, False))
    def partial_update(self, request, *args, **kwargs):
        """
        更新用户组
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除用户组
        """
        return super().destroy(request, *args, **kwargs)

