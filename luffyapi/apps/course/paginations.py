from rest_framework.pagination import  PageNumberPagination as DRFPageNumberPagination
class PageNumberPagination(DRFPageNumberPagination):
    page_size=10  # 后端默认返回的条数
    page_query_param = 'page'  # 返回的参数
    max_page_size = 10  # 最大分页数
    page_size_query_param='page_size' # 前端请求的条数参数