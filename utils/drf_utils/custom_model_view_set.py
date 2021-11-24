# @ProjectName: beer_server
# @FileName: custom_model_view_set.py
# @Author: www
# @Time: 2021/11/24 下午10:16
from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet


class MyListRetrieveDestroyModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                                        GenericViewSet):
    pass
