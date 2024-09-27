from django.urls import path
from .views import ClientUpdateView, ClientListCreate ,ClientDetail, CommandeListCreate,CommandeDetail,  EmployeListCreate , EmployeDetail, MemberListCreate, MemberDetail , LivraisonListCreate , LivraisonDetail , SommeCommandesView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView


urlpatterns = [
    
    
   path('members/', MemberListCreate.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberDetail.as_view(), name='member-detail'),

      path('employes/', EmployeListCreate.as_view(), name='employe-list-create'),
    path('employes/<int:pk>/', EmployeDetail.as_view(), name='employe-detail'),

      # URL pour l'API des clients
    path('clients/', ClientListCreate.as_view(), name='client_list_create'),
    path('clients/<int:pk>/', ClientDetail.as_view(), name='client_detail'),
    path('clients/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
      path('clients/<int:client_id>/somme_commandes/', SommeCommandesView.as_view(), name='somme-commandes'),

    # URL pour l'API des commandes
    path('commandes/', CommandeListCreate.as_view(), name='commande_list_create'),
    path('commandes/<int:pk>/', CommandeDetail.as_view(), name='commande_detail'),

      # URL pour l'API des livraisons
    path('livraisons/', LivraisonListCreate.as_view(), name='livraison_list_create'),
    path('livraisons/<int:pk>/', LivraisonDetail.as_view(), name='livraison_detail'),

     # Endpoint pour l'inscription
    path('api/register/', RegisterView.as_view(), name='register'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
]