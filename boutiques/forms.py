from django import forms

from boutiques.models import Boutique
from algeria_data.wilaya_algerie import WILAYA_CHOICES
from algeria_data.algeria_communes import COMMUNE_CHOICES


class BoutiqueForm(forms.ModelForm):
    wilaya = forms.ChoiceField(
        choices=WILAYA_CHOICES,
        label="Wilaya",
        widget=forms.Select(attrs={'class': 'form-select mb-2'}),
    )
    commune = forms.ChoiceField(
        choices=COMMUNE_CHOICES,
        label="Commune",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Boutique
        fields = ['name', 'wilaya', 'commune', 'phone']
        labels = {
            'name': "Nom de la boutique",
            'phone': "Téléphone",
        }
