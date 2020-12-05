from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin

from . import models
from . import serializer
from . import filters
from .paginations import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend  # 第三方的过滤
from rest_framework.filters import OrderingFilter,SearchFilter # drf自带过滤

class CouresView(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    """查询所有课程"""
    queryset = models.Course.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = serializer.CourseModelSerializer

    pagination_class = PageNumberPagination
    filter_backends=[DjangoFilterBackend,OrderingFilter]
    ordering_fields=['id', 'price', 'students']
    # filter_fields=['course_category','students'] # 使用更为强大的自定义class进行过滤。新支持区间过滤
    filter_class = filters.CourseFilterSet  # 使用filter_class指定，而不是filter_fields


class CourseCategoryView(GenericViewSet,ListModelMixin):
    """
    课程分类查询
    """
    queryset = models.CourseCategory.objects.filter(is_delete=False,is_show=True).order_by("orders")
    serializer_class = serializer.CourseCategorySerializer


class CourseChapterView(GenericViewSet, ListModelMixin):
    queryset = models.CourseChapter.objects.filter(is_delete=False, is_show=True)
    serializer_class = serializer.CourseChapterSerializer

    # 可以按照课程id来查
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']

class CouresSearchView(GenericViewSet,ListModelMixin):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True)
    serializer_class = serializer.CourseModelSerializer
    pagination_class = PageNumberPagination

    filter_backends=[SearchFilter]
    search_fields=['name']