from rest_framework.views import exception_handler
from .response import APIResponse
from .logger import log  # 记录日志

def common_exception_header(exc, context):
    log.error('view is：%s ，error details:%s' % (context['view'].__class__.__name__, str(exc)))
    ret = exception_handler(exc, context)
    if not ret:  # 内置不能处理，准备丢给Django，让我们拦截
        return APIResponse(code=0, msg="error", result=str(exc))  # exc是一个对象，转换为str
    else:
        return APIResponse(code=0, msg="error", result=ret.data)  # ret.data是一个dict