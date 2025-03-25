from django.urls import path,include
from .import views

urlpatterns = [
  #  path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('results/', views.results, name='results'),
    path('upload/', views.upload, name='upload'),
]