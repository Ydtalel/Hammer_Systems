from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)

urlpatterns = [
    path('activate/', views.activate_invite, name='activate_invite'),
    path('referral_list/', views.referral_list, name='referral_list'),
    path('', include(router.urls)),
]
