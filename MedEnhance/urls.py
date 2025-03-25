"""from django.urls import path,include
from .import views

urlpatterns = [
  #  path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('results/', views.results, name='results'),
    path('upload/', views.upload, name='upload'),
]
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView
from .views import  CustomPasswordResetConfirmView, CustomPasswordResetView

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('signup/', views.user_signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('results/', views.results, name='results'),
    path('upload/', views.upload, name='upload'),
    #path('signup/', views.login, name='login'),
    path('password_reset/done/', TemplateView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', TemplateView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    #Admin Dashboard
    #path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    #path('verify-hospital-id/<int:verification_id>/', views.verify_hospital_id, name='verify_hospital_id'),
]

""" # Forgot Password URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete'), 
         name='password_reset_complete'),
    """