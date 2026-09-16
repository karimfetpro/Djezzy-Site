from django.db import models
from django.core.validators import MinValueValidator

from comptes.models import Clients
from boutiques.models import Boutique
from catalogue.models import SubOffers

class Order(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmée'
        CANCELLED = 'cancelled', 'Annulée'

    client = models.ForeignKey( Clients, on_delete=models.CASCADE, related_name='orders' )
    boutique = models.ForeignKey( Boutique, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande #{self.pk} — {self.client.name} ({self.get_status_display()})"
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def cancel(self):
        if self.status != self.Status.CONFIRMED:
            self.status = self.Status.CANCELLED
            self.save(update_fields=['status', 'updated_at'])
        return self.status == self.Status.CANCELLED

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    sub_offer = models.ForeignKey(SubOffers, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.quantity} {self.sub_offer.name}"

    def subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.sub_offer.price
        super().save(*args, **kwargs)
        
def try_confirm_order(order):
    if order.status != Order.Status.PENDING:
        return order.status == Order.Status.CONFIRMED

    items = order.items.all()

    if all(item.sub_offer.quota_restant() >= item.quantity for item in items):
        for item in items:
            item.sub_offer.commandes_effectuees += item.quantity
            item.sub_offer.save()
        order.status = Order.Status.CONFIRMED
        order.save()
        return True

    return False