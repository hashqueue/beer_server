from rest_framework import permissions

from .serializers import TestCaseSerializer
from .models import TestCase
from utils.drf_utils.custom_model_view_set import CustomModelViewSet


# Create your views here.

class TestCasesViewSet(CustomModelViewSet):
    queryset = TestCase.objects.filter(deleted=False).order_by('-id')
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["用例管理"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
