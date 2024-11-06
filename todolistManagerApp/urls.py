from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create/', views.create_task, name='create_task'),
    path('', views.task_list, name='task_list'),
    path('update_status/', views.update_task_status, name='update_task_status'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout_success.html'), name='logout'),
    path('accounts/login/', views.register, name='register'),
]
