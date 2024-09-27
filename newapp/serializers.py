from rest_framework import serializers
from .models import Member, Employe, Commande, Client, Livraison
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    employe_commande = serializers.PrimaryKeyRelatedField(
        queryset=Employe.objects.none(),  # Éviter les requêtes au niveau du module
        required=False,
        allow_null=True
    )

    class Meta:
        model = Commande
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CommandeSerializer, self).__init__(*args, **kwargs)
        self.fields['employe_commande'].queryset = Employe.objects.filter(type_employe='commande')



class LivraisonSerializer(serializers.ModelSerializer):
    commande = serializers.PrimaryKeyRelatedField(queryset=Commande.objects.all())
    employe_livraison = serializers.PrimaryKeyRelatedField(
        queryset=Employe.objects.none(),  # Éviter les requêtes au niveau du module
        required=False,
        allow_null=True
    )

    class Meta:
        model = Livraison
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LivraisonSerializer, self).__init__(*args, **kwargs)
        self.fields['employe_livraison'].queryset = Employe.objects.filter(type_employe='livraison')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # Utilisez le modèle d'utilisateur personnalisé
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user

