from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('ward/add/', views.WardAddView.as_view(), name='ward_add'),
    path('admin/', admin.site.urls),
]
