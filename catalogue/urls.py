from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_manage, name='catalog_manage'),
    path('/categorie/create/', views.categorie_create, name='categorie_create'),
    path('/categorie/update', views.categorie_update, name='categorie_update'),
    path('/categorie/delete', views.categorie_delete, name='categorie_delete'),
    path('/offer/create/', views.offer_create, name='offer_create'),
    path('/offer/uppdate/', views.OfferForm, name ='offer_update'),
    path('/offer/delete/', views.offer_delete, name='offer_delete'),
    path('/suboffer/create/', views.suboffer_create, name='suboffer_create'),
    path('/suboffer/update/', views.suboffer_update, name='suboffer_update'),
    path('/suboffer/delete/', views.suboffer_delete, name='suboffer_delete'),
]