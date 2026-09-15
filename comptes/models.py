from django.db import models
from django.contrib.auth.models import User


class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile', blank = True, default = 1 )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    telephone = models.CharField(max_length=20, blank=False, null=True)
  
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    
class Commercials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='commercial_profile', blank = True, default = 1)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False, null=True)
    telephone = models.CharField(max_length=20, blank=False, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commerciaux"

    def __str__(self):
        return f"{self.prenom} {self.nom}"
