from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Ajoute des champs supplémentaires si nécessaire
    pass
class Member(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    num_telephone = models.BigIntegerField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('conge', 'En congé'),
        ('retire', 'Retiré'),
    ]
    
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    
    TYPE_EMPLOYE_CHOICES = [
        ('commande', 'Gestion des commandes'),
        ('livraison', 'Gestion des livraisons'),
    ]
    
    type_employe = models.CharField(max_length=10, choices=TYPE_EMPLOYE_CHOICES)

    def __str__(self):
        return f'{self.nom} ({self.type_employe})'

class Client(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    num_telephone = models.BigIntegerField()
    carte_identite = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nom

    
    def somme_commandes(self, date_debut, date_fin):
        # Convertir les chaînes en objets datetime
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d")

        # Filtrer les commandes et calculer la somme
        total = self.commandes.filter(
            date_commande__gte=date_debut,
            date_commande__lte=date_fin
        ).aggregate(Sum('total'))['total__sum']
        
        # Retourner le total, ou 0 si aucun résultat
        return total if total is not None else 0

   


  

class Commande(models.Model):
    date_commande = models.DateTimeField()
    quantite = models.IntegerField()
    poids = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('livre', 'Livré'),
        ('annule', 'Annulé'),
    ]
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commandes')
    employe_commande = models.ForeignKey(
        Employe,
        on_delete=models.SET_NULL,
        null=True,
       
    )

    def __str__(self):
        return f'Commande {self.id} - {self.client.nom}'



class Livraison(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='livraisons')
    date_livraison = models.DateTimeField()
    adresse_livraison = models.CharField(max_length=255)
    employe_livraison = models.ForeignKey(
        Employe,
        on_delete=models.SET_NULL,
        null=True,
       
    )

    def __str__(self):
        return f'Livraison {self.id} - Commande {self.commande.id}'
