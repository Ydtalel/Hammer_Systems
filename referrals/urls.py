# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-verification-code/', views.UserProfileViewSet.as_view({'post': 'send_verification_code'}),
         name='send-verification-code'),
    path('verify-code/', views.UserProfileViewSet.as_view({'put': 'verify_code'}), name='verify-code'),  # Изменили метод на PUT
    path('profile/', views.UserProfileViewSet.as_view({'get': 'profile'}), name='profile'),  # Изменили путь и метод
    path('activate-invite/', views.UserProfileViewSet.as_view({'post': 'activate_invite'}), name='activate-invite'),
    path('referred-users/', views.UserProfileViewSet.as_view({'get': 'referred_users'}), name='referred-users'),  # Изменили путь и метод
]
