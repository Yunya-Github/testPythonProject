from django.urls import path, re_path
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register("",views.LoginView,"login")
router.register("register",views.RegisterView,"register")  # 重写create方法，不能使用actions为其重命名。所以在这里用register给create命名
router.register("",views.Chcek_phone_And_send_code,"Chcek_phone_And_send_code")


urlpatterns = [

]

urlpatterns.extend(router.urls)