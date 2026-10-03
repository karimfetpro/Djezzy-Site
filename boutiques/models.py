from django.db import models
from comptes.models import Clients
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Le numéro de téléphone doit être au format valide (ex: +213551234567)."
)

class Boutique(models.Model):

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        ACCEPTEE = 'acceptee', 'Acceptée'
        REFUSEE = 'refusee', 'Refusée'

    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='boutiques')
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    commune = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE)

    class Meta:
        verbose_name = "Boutique"
        verbose_name_plural = "Boutiques"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.client})"