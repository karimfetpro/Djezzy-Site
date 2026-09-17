from django.urls import path
from commandes import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('creer/<int:sub_offer_pk>/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/annuler/', views.order_cancel, name='order_cancel'),

    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/ajouter/<int:sub_offer_id>/", views.cart_add, name="cart_add"),
    path("cart/supprimer/<int:sub_offer_id>/", views.cart_remove, name="cart_remove"),
    path("cart/confirmer/", views.cart_confirm, name="cart_confirm"),
]
