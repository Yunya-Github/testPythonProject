import re

from django.core.cache import cache
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_payload_handler

from . import models

class ManyLoginSerilaize(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ["username", "password", "id"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        # 多方式登录，获取user对象
        print("run...")
        user = self._get_user(attrs)
        # 签发token
        token = self._get_token(user)  # 传入user对象，生成荷载payload
        self.context['token'] = token  # context，默认是一个空对象
        self.context['user'] = user
        return attrs

    def _get_user(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if re.match("^1[3-9][0-9]{9}$", username):
            user = models.User.objects.filter(telephone=username).first()
        elif re.match("^.+@\..+$", username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError("密码错误")
        else:
            raise ValidationError("用户不存在")

    def _get_token(self, user):
        print(user)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class CodeLoginSerilaizer(serializers.ModelSerializer):
    code = serializers.CharField()
    telephone = serializers.CharField()  # 必须在这里替换掉数据库中的unique验证，数据库验证在序列类验证之前

    # 数据库中没有该字段，所以写在这里.
    # 该类主要验证验证码和手机号，不用往数据库中录入，所以全部是read_only
    class Meta:
        model = models.User
        fields = ["telephone", "code"]


    def validate(self, attrs):
        # 查询用户是否存在
        user = self._get_user(attrs)
        # 签发token
        token = self._get_token(user)
        self.context["token"] = token
        self.context["user"] = user
        return attrs

    def _get_user(self, attrs):

        telephone = attrs.get("telephone")
        code = attrs.get("code")

        # 取出缓存中的code，与前端发过来的code做比对
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code:
            # 由于在之前会经过手机号的认证，所以能走到这里手机号一定存在，即代表用户一定存在
            user = models.User.objects.filter(telephone=telephone).first()
            # 删除缓存中的验证码
            cache.set(settings.PHONE_CACHE_KEY % telephone, "")
            return user
        else:
            raise ValidationError("验证码错误")

    def _get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class UserRegisterSerilaizer(serializers.ModelSerializer):
    # 短信验证码发送在手机上，前端不予任何返回。我可以不给你，但是你必须带上，就是write_only
    # 反之，read_only就是我可以不要，但是你必须得看
    code = serializers.CharField(max_length=4, min_length=4, write_only=True)

    class Meta:
        model = models.User
        fields = ['telephone', 'code', 'password', 'username']
        extra_kwargs = {
            'password': {'max_length': 18, 'min_length': 8},
            'username': {'read_only': True}
        }

    def validate(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        # 取出原来的code
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code:
            # 验证码通过
            if re.match('^1[3-9][0-9]{9}$', telephone):
                attrs['username'] = telephone  # 把用户的名字设成手机号
                attrs.pop('code')
                return attrs
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')

    # 重写create方法,否则密码将是密文。
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user