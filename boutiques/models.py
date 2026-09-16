from django.db import models
from comptes.models import Clients
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Le numéro de téléphone doit être au format valide (ex: +213551234567)."
)

class Boutique(models.Model):
    client = models.ForeignKey( Clients, verbose_name=(""), on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    commune = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    statut =models.CharField(max_length=20, choices=[('En attente', 'En attente'), ('Acceptée', 'Acceptée'), ('Refuseé', 'Refuseé')], default='En attente')