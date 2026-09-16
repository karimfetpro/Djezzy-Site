from django import forms
from .models import Boutique


class BoutiqueForm(forms.ModelForm):
    class Meta:
        model = Boutique
        fields = ['name', 'address', 'phone', 'commune']
        labels = {
            'name': "Nom de la boutique",
            'address': "Adresse",
            'phone': "Téléphone",
            'commune': "Commune",
        }