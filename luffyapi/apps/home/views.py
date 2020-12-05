from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django.conf import settings

from . import serializer
from . import models

class BannerView(GenericViewSet, ListModelMixin):
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by("orders")[
               :settings.BANNER_COUNTER]
    serializer_class = serializer.BannerModelSerilaizer

    @action(methods=["GET"], detail=False, url_path="banner",url_name="banner")
    # 使用url_path，自动生成路由时将会以banner/作为匹配
    def get_banner(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
