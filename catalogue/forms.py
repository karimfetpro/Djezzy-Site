from django import forms
from catalogue.models import Categories, Offers, SubOffers


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
        fields = ['offer', 'name', 'price', 'image', 'features', 'quota']
        labels = {
            'offer': "Offre",
            'name': "Nom de la sous-offre",
            'price': "Prix (DA)",
            'image': "Image",
            'features': "Détails (JSON)",
            'quota': "Quota (commandes max)",
        }