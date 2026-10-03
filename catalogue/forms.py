from django import forms
from catalogue.models import Categories, Offers, SubOffers, SubOfferQuota


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['type']
        labels = {'type': "Nom de la catégorie"}


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['categorie', 'name', 'description', 'image']
        labels = {
            'categorie': "Catégorie",
            'name': "Nom de l'offre",
            'description': "Description",
            'image': "Image",
        }



class SubOfferForm(forms.ModelForm):
    class Meta:
        model = SubOffers
        fields = ['offer', 'name', 'price', 'image', 'features']
        labels = {
            'offer': "Offre",
            'name': "Nom de la sous-offre",
            'price': "Prix (DA)",
            'image': "Image",
            'features': "Détails (JSON)",
        }


class QuotaForm(forms.ModelForm):
    class Meta:
        model = SubOfferQuota
        fields = ['commune', 'quota_total']
        labels = {
            'commune': "Commune",
            'quota_total': "Stock total alloué",
        }

    def __init__(self, *args, sub_offer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._sub_offer = sub_offer

    def clean_commune(self):
        commune = self.cleaned_data['commune']
        qs = SubOfferQuota.objects.filter(sub_offer=self._sub_offer, commune__iexact=commune)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Un quota existe déjà pour cette commune sur cette sous-offre.")
        return commune

    def save(self, commit=True):
        self.instance.sub_offer = self._sub_offer
        return super().save(commit=commit)