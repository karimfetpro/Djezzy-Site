from django.db import models
from catalogue.models import SubOffers


class QuotaConsommation(models.Model):
    sub_offer = models.ForeignKey(SubOffers, on_delete=models.CASCADE, related_name='consommations')
    quantite = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Consommation de quota"
        verbose_name_plural = "Consommations de quota"
        ordering = ['-date']

    def __str__(self):
        return f"{self.quantite} sur {self.sub_offer.name} ({self.date:%d/%m/%Y})"
