import re

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from luffyapi.utils.response import APIResponse
from . import serializer
from . import models
from .throttlings import SMSThrotting

class LoginView(ViewSet):
    @action(methods=["POST"],detail=False,url_path="login",url_name="login")
    def login(self,request,*args,**kwargs):
        ser = serializer.ManyLoginSerilaize(data=request.data)
        if ser.is_valid():
            token = ser.context["token"]
            username = ser.context["user"].username
            return APIResponse(token=token,username=username)
        return APIResponse(code=0,msg=ser.errors)

    @action(methods=["POST"],detail=False,url_path="code_login",url_name="code_login")
    def code_login(self,request,*args,**kwargs):
        ser = serializer.CodeLoginSerilaizer(data=request.data)
        if ser.is_valid(raise_exception=True):
            token = ser.context["token"]
            username = ser.context["user"].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)


class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserRegisterSerilaizer

    # 覆写父类create直接使用即可，返回APIResponse对象
    # 为什么不用actions装饰器？因为它会自动生成一个 user/ post允许的接口。
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data.get("username")
        return APIResponse(code=1, msg="注册成功", username=username)


class Chcek_phone_And_send_code(ViewSet):
    @action(methods=["GET"],detail=False,url_path="check_telephone",url_name="check_telephone")
    def check(self,request,*args,**kwargs):
        telephone = request.query_params.get("telephone")
        if not re.match("^1[3-9][0-9]{9}", telephone):
            return APIResponse(code=0, msg="手机号不合法")
        try:
            models.User.objects.get(telephone=telephone)
            return APIResponse(code=1)
        except Exception:
            return APIResponse(code=0,msg="手机号不存在")

    @action(methods=["GET"], detail=False, url_path="send", url_name="send",throttle_classes=[SMSThrotting])
    def send(self,request,*args,**kwargs):
        from luffyapi.libs.tx_sms import get_code,send_message
        from django.core.cache import cache  # 如不设置缓存默认保存在内存中
        telephone = request.query_params.get("telephone")
        code = get_code()
        result = send_message(telephone, code)

        cache.set(settings.PHONE_CACHE_KEY % telephone, code, 180)  # 存储三分钟
        if result:
            return APIResponse(code=1, msg='验证码发送成功')
        else:
            return APIResponse(code=0, msg='验证码发送失败')

