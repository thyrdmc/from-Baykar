from django.urls import path, re_path
from django.shortcuts import render

from . import views


urlpatterns = [
    path('register/', views.register, name='register-user'),

    path('login/', views.login, name='login'),

    path('reset_password/',  views.reset_password, name='reset_password'),

    path('forgot_password/',  views.forgot_password, name='forgot_password'),


    path('vehicles/create/', views.create_vehicle, name='create-vehicle'),
    
    path('vehicles/', views.vehicles, name='vehicles'),

    path('vehicles/<int:pk>/', views.get_vehicle, name='detail-vehicle'),

    path('vehicles/<int:pk>/update/', views.update_vehicle, name='update-vehicle'),

    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete-vehicle'),
]