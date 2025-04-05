from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
import os
from .views import results
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_IMAGE_DIR = os.path.join(BASE_DIR, 'InputImages')
OUTPUT_IMAGE_DIR = os.path.join(BASE_DIR, 'OutputImages')

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('results/', views.results, name='results'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    
    path('upload/', views.upload_image, name='upload_image'),
    path('results/<int:image_id>/', results, name='results'),
    re_path(r'^input-images/(?P<path>.*)$', serve, {'document_root': INPUT_IMAGE_DIR}),
    re_path(r'^output-images/(?P<path>.*)$', serve, {'document_root': OUTPUT_IMAGE_DIR}),
]
