from django import forms
from catalogue.models import Categories, Offers, SubOffers, SubOfferQuota
from algeria_data import wilaya_algerie
from algeria_data import algeria_communes

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
    wilaya = forms.ChoiceField(
        choices=wilaya_algerie.WILAYA_CHOICES,
        label="Wilaya",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    commune = forms.ChoiceField(
        choices=algeria_communes.COMMUNE_CHOICES,
        label="Commune",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    class Meta:
        model = SubOfferQuota
        fields = ['wilaya', 'commune', 'quota_total']
        labels = {
            'wilaya': "Wilaya",
            'commune': "Commune",
            'quota_total': "Stock total alloué",
        }

    def __init__(self, *args, sub_offer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._sub_offer = sub_offer

    def save(self, commit=True):
        self.instance.sub_offer = self._sub_offer
        return super().save(commit=commit)