from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from comptes.models import Clients

class ClientRegisterForm(UserCreationForm):
 
    nom = forms.CharField(max_length=100, label="Nom")
    prenom = forms.CharField(max_length=100, label="Prénom") 
    email = forms.EmailField(label="Adresse e-mail")
    phone = forms.CharField(max_length=15, label="Téléphone")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Clients.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Clients.objects.create(
             user=user,
             nom=self.cleaned_data['nom'],
             prenom=self.cleaned_data['prenom'],
             email=self.cleaned_data['email'],
             telephone=self.cleaned_data['phone'],
            )
           
        return user
        
