from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('activate/', views.activate_invite, name='activate_invite'),
    path('referral_list/', views.referral_list, name='referral_list'),
]
