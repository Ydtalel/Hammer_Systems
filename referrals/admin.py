from django.contrib import admin
from .models import UserProfile, VerificationCode


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'invite_code', 'referred_by')
    list_filter = ('referred_by',)
    search_fields = ('phone_number', 'invite_code')


class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__phone_number', 'code')
    date_hierarchy = 'created_at'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)

