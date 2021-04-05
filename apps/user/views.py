from rest_framework import permissions, status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.custom_json_response import JsonResponse
from .serializers import CurrentUserInfoSerializer, UserRegisterSerializer, MyTokenObtainPairSerializer
from .models import User


# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        用户登录
        * `username`字段可填写用户的`username`或`email`,只要填写的数据正确都可以`登录成功`
        * 响应体中`access`就是JWT的`token`值,用于访问其他接口时做认证使用
        """
        return super().post(request, *args, **kwargs)


class GetAndUpdateCurrentLoginUserInfoView(RetrieveUpdateAPIView):
    queryset = User.objects.all().order_by('-id')
    serializer_class = CurrentUserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["用户信息管理"]

    def get(self, request, *args, **kwargs):
        """
        获取`用户`的`个人信息`
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        修改`用户`的`个人信息`
        * 全部字段修改
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        修改`用户`的`个人信息`
        * 部分字段修改
        """
        return self.partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 1.当前请求该接口的用户是要查看的用户数据对象的owner时,才会返回用户数据
        # 2.当前请求该接口的用户的is_staff为1时才会返回用户的数据
        if instance.id == request.user.id or request.user.is_staff == 1:
            serializer = self.get_serializer(instance)
            return JsonResponse(data=serializer.data, msg='获取用户信息成功', code=20000, status=status.HTTP_200_OK)
        return JsonResponse(data=[], msg='您无权限查看该用户的信息', code=40003, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.id == request.user.id or request.user.is_staff == 1:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return JsonResponse(data=serializer.data, msg='修改用户信息成功', code=20000, status=status.HTTP_200_OK)
        return JsonResponse(data=[], msg='您无权限修改该用户的信息', code=40003, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg='注册成功,请登录', code=20000, status=status.HTTP_201_CREATED,
                            headers=headers)

    def post(self, request, *args, **kwargs):
        """
        用户注册
        * `所有字段`都是`必填项`
        """
        return super().post(request, *args, **kwargs)
