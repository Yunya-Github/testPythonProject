from django_filters import FilterSet
from django_filters import filters
from . import models


class CourseFilterSet(FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")  # 可以根据价格查询，小于或等于这个价格
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = models.Course
        fields = ["course_category","students"]  # 还可以根据分类查询与热度查询
