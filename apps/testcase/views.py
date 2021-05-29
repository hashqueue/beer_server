from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from config.models import Config
from utils.drf_utils.custom_json_response import JsonResponse
from .serializers import TestCaseSerializer, RunTestCaseSerializer
from .models import TestCase
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from utils.http_utils.request import run_testcase
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups


# Create your views here.
@extend_schema(tags=['用例管理'])
class TestCasesViewSet(CustomModelViewSet):
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
