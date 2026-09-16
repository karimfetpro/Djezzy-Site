from django.urls import path
from . import views

urlpatterns = [
    path('', views.boutique_list, name='boutique_list'),
    path('add/',views.boutique_create, name='add'),
    path('<int:pk>/update/', views.boutique_update, name='boutique_update'),
    path('delete/', views.boutique_delete, name='delete'),
]
