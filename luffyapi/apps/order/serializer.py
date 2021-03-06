from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from course.models import Course
from . import models

class OrderSerializer(serializers.ModelSerializer):
    # 因为传入的课程可能在购物车中是[1,2,3]的pk
    # 所以通过PrimaryKeyRelatedField之间进行查询，拿到[obj1,obj2,obj3]
    # order表和Course表没有任何关系
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['total_amount', 'subject', 'pay_type', 'course']
        # 有默认值就不是必填，规定一下，必须填入
        extra_kwargs = {
            'total_amount': {'required': True},
            'pay_type': {'required': True},
        }

    def validate(self, attrs):
        # 1）订单总价校验
        total_amout = self._check_price(attrs)
        # 2）生成订单号
        out_trade_no = self._gen_out_trade_no()
        # 3）支付用户：request.user
        user = self._get_user()
        # 4）支付链接生成
        pay_url = self._gen_pay_url(out_trade_no, total_amout, attrs.get('subject'))
        # 5）入库(两个表)的信息准备
        self._before_create(attrs, user, pay_url, out_trade_no)
        return attrs

    def _check_price(self, attrs):
        total_amount = attrs.get('total_amount')
        course_list = attrs.get('course')
        total_price = 0
        for course in course_list:
            total_price += course.price
        if total_price != total_amount:
            raise ValidationError('价格不合法')

        return total_amount

    def _gen_out_trade_no(self):
        import uuid
        return str(uuid.uuid4()).replace('-', '')

    def _get_user(self):
        # 需要request对象(需要视图通过context把reuqest对象传入。重写create方法)
        request = self.context.get('request')
        return request.user

    def _gen_pay_url(self, out_trade_no, total_amout, subject):
        # total_amout是Decimal类型，识别不了，需要转换成float类型
        from luffyapi.libs.al_pay import alipay, gateway
        from django.conf import settings
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=float(total_amout),
            subject=subject,
            return_url=settings.RETURN_URL,  # get回调，前台地址
            notify_url=settings.NOTIFY_URL  # post回调，后台地址
        )
        return gateway + order_string

    def _before_create(self, attrs, user, pay_url, out_trade_no):
        attrs['user'] = user
        attrs['out_trade_no'] = out_trade_no

        self.context['pay_url'] = pay_url



    def create(self, validated_data):
        # 创建订单记录
        course_list = validated_data.pop('course')
        order = models.Order.objects.create(**validated_data)
        for course in course_list:
            models.OrderDetail.objects.create(order=order, course=course, price=course.price, real_price=course.price)

        return order

