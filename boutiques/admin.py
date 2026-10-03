from django.contrib import admin
from boutiques.models import Boutique

@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'address', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'address', 'phone', 'client__nom')
    ordering = ('name',)