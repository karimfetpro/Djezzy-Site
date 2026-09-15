from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_views, name='register'),
    path('login/', views.login_views, name='login'),
]
