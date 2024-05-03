from django.urls import path, re_path
from django.shortcuts import render

from . import views


urlpatterns = [
    path('register/', views.register, name='register-user'),

    path('login/', views.login, name='login'),

    path('reset_password/',  views.reset_password, name='reset_password'),

    path('forgot_password/',  views.forgot_password, name='forgot_password'),

]