from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('article/<int:pk>/', views.ArticleView.as_view(), name='article'),
    path('articles/', views.ArticlesView.as_view(), name='articles'),
    path('articles/liked/', views.ArticlesLikedView.as_view(), name='articles_liked'),
    path('articles/read/', views.ArticlesReadView.as_view(), name='articles_read'),
    path('articles/<str:slug>/', views.ArticlesByTagView.as_view(), name='articles_by_tag'),
    path('ward/add/', views.WardAddView.as_view(), name='ward_add'),
    path('ward/<int:pk>/', views.WardView.as_view(), name='ward'),
    path('admin/', admin.site.urls),
]
