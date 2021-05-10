from drf_spectacular.utils import extend_schema
from rest_framework import permissions

from .serializers import ConfigSerializer
from .models import Config
from utils.drf_utils.custom_model_view_set import CustomModelViewSet


# Create your views here.
@extend_schema(tags=['配置管理'])
class ConfigsViewSet(CustomModelViewSet):
    queryset = Config.objects.all().order_by('-id')
    serializer_class = ConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)
