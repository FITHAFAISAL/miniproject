from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification, HospitalVerification

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_email_verified', 'is_hospital_verified')
    list_filter = ('user_type', 'is_email_verified', 'is_hospital_verified')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'user_type', 'hospital_id')}),
        ('Verification', {'fields': ('is_email_verified', 'is_hospital_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'attempts')
    search_fields = ('user__email', 'user__username')
    list_filter = ('created_at',)

class HospitalVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_status', 'verified_by')
    search_fields = ('user__email', 'user__username')
    list_filter = ('verification_status',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTPVerification, OTPVerificationAdmin)
admin.site.register(HospitalVerification, HospitalVerificationAdmin)
