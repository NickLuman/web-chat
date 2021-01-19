from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.auth_check, name='start'),
    path('me/', views.dashboard, name='dashboard'),  
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('me/create-dialogue/<int:user_id>', login_required
(views.CreateDialogueView.as_view()), name='create dialogue'),
    path('me/dialogue/<int:chat_id>', login_required
(views.MessagesView.as_view()), name='l'),
]