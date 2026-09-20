from django.urls import path
from commandes import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/annuler/', views.order_cancel, name='order_cancel'),

    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:sub_offer_id>/', views.cart_add, name='cart_add'),
    path('panier/retirer/<int:sub_offer_id>/', views.cart_remove, name='cart_remove'),
    path('panier/confirmer/', views.cart_confirm, name='cart_confirm'),
    path('panier/<str:action>/<int:sub_offer_id>/', views.cart_update, name='cart_update'),

    path('en-attente/', views.cart_pending_list, name='cart_pending_list'),
    path('<int:pk>/accepter/', views.accept_cart, name='accept_cart'),
    path('<int:pk>/refuser/', views.refuse_cart, name='refuse_cart'),
]