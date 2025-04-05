from django.contrib import admin
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
from django.contrib import admin
from .models import UploadedImage

class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'uploaded_at')

#admin.site.register(UploadedImage, UploadedImageAdmin)
