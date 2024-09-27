from django import forms
from .models import Client, Commande
from .models import Livraison


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'num_telephone', 'carte_identite']

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['date_commande', 'quantite','poids', 'total', 'statut', 'client','employe_commande']



class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['commande', 'date_livraison', 'adresse_livraison','employe_livraison']

