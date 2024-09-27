import datetime
from django.shortcuts import redirect, render, get_object_or_404
from .models import Member, Client, Commande, Employe, Livraison
from rest_framework import generics
from .serializers import (
    MemberSerializer,
    EmployeSerializer,
    CommandeSerializer,
    ClientSerializer,
    LivraisonSerializer,
    RegisterSerializer,
)
from .forms import ClientForm, CommandeForm, LivraisonForm
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model

# Inscription
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

# Vue pour lister et créer des membres
class MemberListCreate(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

# Vue pour récupérer, mettre à jour et supprimer un membre
class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

# Vue pour lister et créer des employés
class EmployeListCreate(generics.ListCreateAPIView):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer

# Vue pour récupérer, mettre à jour et supprimer un employé
class EmployeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer

# Vue pour lister et créer des clients
class ClientListCreate(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# Vue pour récupérer, mettre à jour et supprimer un client
class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# Vue pour lister et créer des commandes
class CommandeListCreate(generics.ListCreateAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

# Vue pour récupérer, mettre à jour et supprimer une commande
class CommandeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

# Vue pour lister et créer des livraisons
class LivraisonListCreate(generics.ListCreateAPIView):
    queryset = Livraison.objects.all()
    serializer_class = LivraisonSerializer

# Vue pour récupérer, mettre à jour et supprimer une livraison
class LivraisonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livraison.objects.all()
    serializer_class = LivraisonSerializer

class SommeCommandesView(APIView):
    def get(self, request, client_id):
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        if not date_debut or not date_fin:
            return Response(
                {"error": "Les dates de début et de fin sont requises."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            client = Client.objects.get(id=client_id)
            somme = client.somme_commandes(date_debut, date_fin)
            return Response({"somme": somme})
        except Client.DoesNotExist:
            return Response(
                {"error": "Client non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Ceci est une vue protégée"})

def index(request):
    mem = Member.objects.all()
    return render(request, 'index.html', {'mem': mem})

def add(request):
    return render(request, 'add.html')

def addrec(request):
    x = request.POST['first']
    y = request.POST['last']
    z = request.POST['country']
    mem = Member(firstname=x, lastname=y, country=z)
    mem.save()
    return redirect("/")

def delete(request, id):
    mem = Member.objects.get(id=id)
    mem.delete()
    return redirect("/")

def update(request, id):
    mem = Member.objects.get(id=id)
    return render(request, 'update.html', {'mem': mem})

def uprec(request, id):
    x = request.POST['first']
    y = request.POST['last']
    z = request.POST['country']
    mem = Member.objects.get(id=id)
    mem.firstname = x
    mem.lastname = y
    mem.country = z
    mem.save()
    return redirect("/")

def employe_index(request):
    employes = Employe.objects.all()
    return render(request, 'employe_index.html', {'employes': employes})

def employe_add(request):
    return render(request, 'employe_add.html')

def employe_addrec(request):
    nom = request.POST['nom']
    prenom = request.POST['prenom']
    num_tel = request.POST['num_tel']
    salaire = request.POST['salaire']
    statut = request.POST['statut']
    type_employe = request.POST['type_employe']
    employe = Employe(
        nom=nom,
        prenom=prenom,
        num_telephone=num_tel,
        salaire=salaire,
        statut=statut,
        type_employe=type_employe
    )
    employe.save()
    return redirect("/employe")

def employe_delete(request, id):
    employe = Employe.objects.get(id=id)
    employe.delete()
    return redirect("/employe")

def employe_update(request, id):
    employe = Employe.objects.get(id=id)
    return render(request, 'employe_update.html', {'employe': employe})

def employe_uprec(request, id):
    nom = request.POST['nom']
    prenom = request.POST['prenom']
    num_tel = request.POST['num_tel']
    salaire = request.POST['salaire']
    statut = request.POST['statut']
    employe = Employe.objects.get(id=id)
    employe.nom = nom
    employe.prenom = prenom
    employe.num_telephone = num_tel
    employe.salaire = salaire
    employe.statut = statut
    employe.save()
    return redirect("/employe")

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

# Vue pour créer un client
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_form.html', {'form': form})

# Vue pour supprimer un client
def client_delete(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'client_confirm_delete.html', {'client': client})

def somme_commandes_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    # Définissez vos dates de début et de fin
    date_debut = datetime(2024, 1, 1)  # Exemple : 1er janvier 2024
    date_fin = datetime(2024, 8, 31)   # Exemple : 31 août 2024

    # Calculez la somme des commandes
    somme = client.somme_commandes(date_debut, date_fin)

    return render(request, 'somme_commandes.html', {'client': client, 'somme': somme})

# Vue pour lister les commandes
def commande_list(request):
    commandes = Commande.objects.all()
    return render(request, 'commande_list.html', {'commandes': commandes})

# Vue pour créer une commande
def commande_create(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('commande_list')
    else:
        form = CommandeForm()
    return render(request, 'commande_form.html', {'form': form})

# Vue pour mettre à jour une commande
def commande_update(request, id):
    commande = get_object_or_404(Commande, id=id)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('commande_list')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'commande_form.html', {'form': form})

# Vue pour supprimer une commande
def commande_delete(request, id):
    commande = get_object_or_404(Commande, id=id)
    if request.method == 'POST':
        commande.delete()
        return redirect('commande_list')
    return render(request, 'commande_confirm_delete.html', {'commande': commande})

class ClientUpdateView(APIView):
    def put(self, request, pk):
        try:
            # Récupérer l'instance du client par son ID
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error": "Client not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Pré-remplir les champs avec les données existantes
        serializer = ClientSerializer(client, data=request.data)
        
        # Vérifier la validité des données
        if serializer.is_valid():
            # Enregistrer les modifications
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def livraison_list(request):
    livraisons = Livraison.objects.all()
    return render(request, 'livraison_list.html', {'livraisons': livraisons})

def livraison_create(request):
    if request.method == 'POST':
        form = LivraisonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livraison_list')
    else:
        form = LivraisonForm()
    return render(request, 'livraison_form.html', {'form': form})

def livraison_update(request, id):
    livraison = get_object_or_404(Livraison, id=id)
    if request.method == 'POST':
        form = LivraisonForm(request.POST, instance=livraison)
        if form.is_valid():
            form.save()
            return redirect('livraison_list')
    else:
        form = LivraisonForm(instance=livraison)
    return render(request, 'livraison_form.html', {'form': form})

def livraison_delete(request, id):
    livraison = get_object_or_404(Livraison, id=id)
    if request.method == 'POST':
        livraison.delete()
        return redirect('livraison_list')
    return render(request, 'livraison_confirm_delete.html', {'livraison': livraison})
