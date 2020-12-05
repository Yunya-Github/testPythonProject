from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('pay', views.PayView, 'pay')

urlpatterns = [
    path('', include(router.urls)),
    path('success/', views.SuccessView.as_view()),
]
