from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .template_views import menu_root
from .views import UserProfileViewSet, login_view, verify_code_view, profile_view

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('v1', menu_root, name='menu'),
    path('', include(router.urls)),
    path('send-verification-code/', UserProfileViewSet.as_view({'post': 'send_verification_code'}),
         name='send-verification-code'),
    path('verify-code/', UserProfileViewSet.as_view({'put': 'verify_code'}), name='verify-code'),
    path('profile/', UserProfileViewSet.as_view({'get': 'profile'}), name='profile'),
    path('activate-invite/', UserProfileViewSet.as_view({'post': 'activate_invite'}), name='activate-invite'),
    path('referred-users/', UserProfileViewSet.as_view({'get': 'referred_users'}), name='referred-users'),

    path('login/', login_view, name='login'),
    path('verify-code-template/', verify_code_view, name='verify-code'),
    path('profile-template/', profile_view, name='profile'),
]