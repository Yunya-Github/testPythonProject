import os
# 应用号
APPID="2016110400790806"
# 应用私钥
APP_PRIVATE_KEY_STRING = open(os.path.join(os.path.dirname(__file__),'pem','private_key.pem')).read()
# 应用公钥
ALIPAY_PUBLIC_KEY_STRING = open(os.path.join(os.path.dirname(__file__),'pem','al_public_key.pem')).read()
# 加密方式
SIGN_TYPE='RSA2'
DEBUG=True
# 支付宝网关，正式环境和沙箱环境。
GATEWAY='https://openapi.alipaydev.com/gateway.do?' if DEBUG else 'https://openapi.alipay.com/gateway.do?'