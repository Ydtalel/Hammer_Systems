from django.contrib import admin
from .models import UserProfile, VerificationCode


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code', 'referred_by')
    list_filter = ('referred_by',)
    search_fields = ('phone_number', 'invite_code')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VerificationCode)
