from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from config.models import Config
from .serializers import TestCaseSerializer, RunTestCaseSerializer
from .models import TestCase
from utils.http_utils.request import run_testcase
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['用例管理'])
class TestCasesViewSet(ModelViewSet):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]
    filterset_fields = ['testcase_name', 'testcase_desc', 'creator', 'modifier', 'testsuite']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return TestCase.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = TestCase.objects.filter(
                Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset

    @extend_schema(responses=enveloper(RunTestCaseSerializer, False))
    @action(methods=['post'], detail=True, serializer_class=RunTestCaseSerializer)
    def run(self, request, pk=None):
        """
        运行测试用例
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('config_id', False):
            # 选择某个配置来执行用例
            data = run_testcase(testcase=get_object_or_404(TestCase, pk=pk),
                                config=get_object_or_404(Config, pk=request.data.get('config_id')))
            return JsonResponse(data=data, code=20000, msg='运行成功', status=status.HTTP_200_OK)
        else:
            # 不选择配置直接执行用例
            data = run_testcase(testcase=get_object_or_404(TestCase, pk=pk))
            return JsonResponse(data=data, code=20000, msg='运行成功', status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(TestCaseSerializer, False))
    def create(self, request, *args, **kwargs):
        """
        新增用例
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    @extend_schema(responses=enveloper(TestCaseSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取用例列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/testcases/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "teststeps": [
                {
                "id": 0,
                "step_validators": [
                {
                "id": 0,
                "validator_type": "equal_integer",
                "jmespath_expression": "string",
                "expected_value": "string",
                "desc": "string"
                }
                ],
                "teststep_name": "string",
                "method": "GET",
                "url_path": "string",
                "desc": "string",
                "json": {
                "property1": null,
                "property2": null
                },
                "params": {
                "property1": null,
                "property2": null
                },
                "data": {
                "property1": null,
                "property2": null
                },
                "headers": {
                "property1": null,
                "property2": null
                },
                "cookies": {
                "property1": null,
                "property2": null
                },
                "export": {
                "property1": null,
                "property2": null
                },
                "extract": {
                "property1": null,
                "property2": null
                },
                "quote_testcase_id": 4294967295
                }
                ],
                "testsuite_name": "string",
                "project_id": 0,
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "testcase_name": "string",
                "testcase_desc": "string",
                "testsuite": 0
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

    @extend_schema(responses=enveloper(TestCaseSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看用例详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(TestCaseSerializer, False))
    def update(self, request, *args, **kwargs):
        """
        更新用例
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(TestCaseSerializer, False))
    def partial_update(self, request, *args, **kwargs):
        """
        更新用例
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除用例
        """
        return super().destroy(request, *args, **kwargs)
