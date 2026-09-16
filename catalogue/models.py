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
    quota = models.PositiveIntegerField(default=0, verbose_name="Quota (commandes)")
    commandes_effectuees = models.PositiveIntegerField(default=0, verbose_name="Commandes effectuées")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sous-offre"
        verbose_name_plural = "Sous-offres"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.offer.name})"

    def quota_restant(self):
        return max(self.quota - self.commandes_effectuees, 0)

    def quota_atteint(self):
        return self.commandes_effectuees >= self.quota

