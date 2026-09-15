from django.urls import path
from . import views

urlpatterns = [
    path('', views.boutique_list, name='boutique_list'),
    path('add/',views.boutique_create, name='add'),
    path('delete/', views.boutique_delete, name='delete'),
]
