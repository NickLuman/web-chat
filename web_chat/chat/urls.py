from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='start'),  
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]