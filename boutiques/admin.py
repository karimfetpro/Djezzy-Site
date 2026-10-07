from django.contrib import admin
from boutiques.models import Boutique

@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'wilaya', 'commune', 'phone', 'statut', 'created_at')
    list_filter = ('statut', 'wilaya', 'created_at')
    search_fields = ('name', 'wilaya', 'commune', 'phone', 'client__nom')
    ordering = ('name',)
