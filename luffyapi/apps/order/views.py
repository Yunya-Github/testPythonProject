# Create your views here.

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models
from . import serializer


class PayView(GenericViewSet, CreateModelMixin):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderSerializer

    # 重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.context.get('pay_url'))


class SuccessView(APIView):
    def get(self, request, *args, **kwargs):
        out_trade_no = request.query_params.get('out_trade_no')
        order = models.Order.objects.filter(out_trade_no=out_trade_no).first()
        if order.order_status == 1:
            return Response(True)
        else:
            return Response(False)

    def post(self, request, *args, **kwargs):
        '''
        支付宝回调接口
        '''
        from luffyapi.libs.al_pay import alipay
        from luffyapi.utils.logger import log
        data = request.data
        out_trade_no = data.get('out_trade_no', None)
        gmt_payment = data.get('gmt_payment', None)
        signature = data.pop("sign")
        # 验证签名
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            models.Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1, pay_time=gmt_payment)
            log.info('%s订单支付成功' % out_trade_no)
            return Response('success')
        else:
            log.info('%s订单有问题' % out_trade_no)
            return Response('error')
