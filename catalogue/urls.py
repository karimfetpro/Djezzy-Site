from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_manage, name='catalog_manage'),

    path('offres/', views.catalog_view, name='catalog_view'),
    path('offres/<int:pk>/', views.offer_detail, name='offer_detail'),

    path('categorie/create/', views.categorie_create, name='categorie_create'),
    path('categorie/<int:pk>/update/', views.categorie_update, name='categorie_update'),
    path('categorie/<int:pk>/delete/', views.categorie_delete, name='categorie_delete'),

    path('offer/create/', views.offer_create, name='offer_create'),
    path('offer/<int:pk>/update/', views.offer_update, name='offer_update'),
    path('offer/<int:pk>/delete/', views.offer_delete, name='offer_delete'),

    path('suboffer/create/', views.suboffer_create, name='suboffer_create'),
    path('suboffer/<int:pk>/update/', views.suboffer_update, name='suboffer_update'),
    path('suboffer/<int:pk>/delete/', views.suboffer_delete, name='suboffer_delete'),

    path('suboffer/<int:sub_offer_pk>/quotas/', views.quota_list, name='quota_list'),
    path('suboffer/<int:sub_offer_pk>/quotas/create/', views.quota_create, name='quota_create'),
    path('quotas/<int:pk>/update/', views.quota_update, name='quota_update'),
    path('quotas/<int:pk>/delete/', views.quota_delete, name='quota_delete'),
]