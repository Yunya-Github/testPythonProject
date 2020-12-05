from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("",views.BannerView)

urlpatterns = [

]

urlpatterns.extend(router.urls)
