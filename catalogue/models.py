from django.db import models

class Categories(models.Model):
    type = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['type']

    def __str__(self):
        return self.type


class Offers(models.Model):
    categorie = models.ForeignKey( Categories, on_delete=models.CASCADE, related_name='offers' )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='sous_offres/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Offre"
        verbose_name_plural = "Offres"
        ordering = ['name']

    def __str__(self):
        return self.name


class SubOffers(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='sub_offers')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='sous_offres/', blank=True, null=True)
    features = models.JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "Sous-offre"
        verbose_name_plural = "Sous-offres"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.offer.name})"

    def quota_restant(self, commune):
        """Stock restant pour CETTE sous-offre, dans UNE commune donnée.
        Si aucun quota n'a été défini pour cette commune, le stock est 0
        (pas de vente possible tant qu'un quota n'a pas été explicitement alloué)."""
        quota = self.quotas.filter(commune=commune).first()
        return quota.remaining if quota else 0


class SubOfferQuota(models.Model):
    
    sub_offer = models.ForeignKey(SubOffers, on_delete=models.CASCADE, related_name='quotas')
    commune = models.CharField(max_length=100)
    quota_total = models.PositiveIntegerField(help_text="Stock total alloué pour cette commune.")
    quantity_sold = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Quota par commune"
        verbose_name_plural = "Quotas par commune"
        constraints = [
            models.UniqueConstraint(
                fields=['sub_offer', 'commune'],
                name='unique_quota_sub_offer_commune'
            )
        ]
        ordering = ['commune', 'sub_offer__name']

    def __str__(self):
        return f"{self.sub_offer.name} — {self.commune} ({self.remaining}/{self.quota_total})"

    @property
    def remaining(self):
        return max(self.quota_total - self.quantity_sold, 0)

    @property
    def is_available(self):
        return self.remaining > 0