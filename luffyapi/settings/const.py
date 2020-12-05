# 首页轮播图个数
BANNER_COUNTER=3

# 手机验证码缓存KEY
PHONE_CACHE_KEY = "sms_cache_%s"

# 缓存到redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",  # 自定义的协议
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}