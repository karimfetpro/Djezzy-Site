from django.urls import path
from commandes import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('creer/<int:sub_offer_pk>/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/annuler/', views.order_cancel, name='order_cancel'),
]