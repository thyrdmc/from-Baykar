from django.urls import path, re_path
from django.shortcuts import render

from . import views


urlpatterns = [
    path('register/', views.register, name='register-user'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),
    

    path('reset_password/', views.reset_password, name='reset_password'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),


    path('vehicles/create/', views.create_vehicle, name='create-vehicle'),
    
    path('vehicles/', views.vehicles, name='vehicles'),

    path('vehicles/<int:pk>/', views.get_vehicle, name='detail-vehicle'),

    path('vehicles/<int:pk>/update/', views.update_vehicle, name='update-vehicle'),

    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete-vehicle'),


    path('rent-vehicle/', views.rent_vehicle, name='rent_vehicle'),

    path('rental-records/', views.rental_records, name='rental_records'),

     path('rental-records/<int:pk>/', views.get_rental_record, name='detail-rental-record'),

    path('rental-records/<int:pk>/update/', views.update_rental_record, name='update-rental-record'),

    path('rental-records/<int:pk>/delete/', views.delete_rental_record, name='delete-rental-record'),

    
]