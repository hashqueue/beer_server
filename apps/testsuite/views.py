from rest_framework import permissions

from .serializers import TestSuiteSerializer
from .models import TestSuite
from utils.drf_utils.custom_model_view_set import CustomModelViewSet


# Create your views here.

class TestSuitesViewSet(CustomModelViewSet):
    queryset = TestSuite.objects.filter(deleted=False).order_by('-id')
    serializer_class = TestSuiteSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["套件管理"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
