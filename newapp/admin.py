from django.contrib import admin
from .models import Member , Employe ,Client , Commande , Livraison , CustomUser

class MemberAdmin(admin.ModelAdmin):
    list_display="firstname","lastname","country"

admin.site.register(Member,MemberAdmin)

class EmployeAdmin(admin.ModelAdmin):
    list_display="nom","prenom","num_telephone","salaire","statut","type_employe"

admin.site.register(Employe,EmployeAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display="nom","prenom","adresse","num_telephone","carte_identite"

admin.site.register(Client,ClientAdmin)

class CommandeAdmin(admin.ModelAdmin):
    list_display="date_commande","quantite","poids","total","statut","client","employe_commande"

admin.site.register(Commande,CommandeAdmin)

class LivraisonAdmin(admin.ModelAdmin):
    list_display="commande","date_livraison","adresse_livraison","employe_livraison"

admin.site.register(Livraison,LivraisonAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(CustomUser,CustomUserAdmin)