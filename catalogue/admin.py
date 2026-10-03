from django.contrib import admin
from catalogue.models import Offers, SubOffers, Categories, SubOfferQuota


class SubOfferQuotaInline(admin.TabularInline):
    model = SubOfferQuota
    extra = 1
    readonly_fields = ['quantity_sold']


@admin.register(SubOffers)
class SubOffersAdmin(admin.ModelAdmin):
    list_display = ('name', 'offer', 'price', 'created_at')
    list_filter = ('offer__categorie', 'offer')
    search_fields = ('name', 'offer__name')
    inlines = [SubOfferQuotaInline]


@admin.register(SubOfferQuota)
class SubOfferQuotaAdmin(admin.ModelAdmin):
    list_display = ('sub_offer', 'commune', 'quota_total', 'quantity_sold', 'remaining')
    list_filter = ('commune',)
    search_fields = ('sub_offer__name', 'commune')
    readonly_fields = ('quantity_sold',)

    def remaining(self, obj):
        return obj.remaining
    remaining.short_description = "Stock restant"


admin.site.register(Offers)
admin.site.register(Categories)