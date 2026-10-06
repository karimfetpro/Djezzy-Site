from django import forms
from boutiques.models import Boutique
from algeria_data import algeria_communes, wilaya_algerie

class BoutiqueForm(forms.ModelForm):
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
        model = Boutique
        fields = ['name', 'commune', 'wilaya', 'phone']
        labels = {
            'name': "Nom de la boutique",
            'wilaya': "Wilaya",
            'commune': "Commune",
            'phone': "Téléphone",
        }
 