from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    hospital_id = models.CharField(max_length=20, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_hospital_verified = models.BooleanField(default=False)

class OTPVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)

class HospitalVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verification_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ), default='pending')
    admin_notes = models.TextField(null=True, blank=True)
    verified_by = models.ForeignKey(CustomUser, related_name='verified_users', 
                                    null=True, blank=True, on_delete=models.SET_NULL)
    
    