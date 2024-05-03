from django.urls import path, re_path
from django.shortcuts import render

from . import views


urlpatterns = [
    path("", views.homepage),

]