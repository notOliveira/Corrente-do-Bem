# Views, viewsets e generics da aplicação apis
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import CreateSuperUserPermission
# 
from organizations.models import Donation, OrganizationProfile, UserRole
from users.models import Profile
from invitations.models import Invitation
from users.models import CustomUser
from rest_framework.permissions import AllowAny
# Serializers
from .serializers.donations_serializer import DonationSerializer
from .serializers.organization_profile_serializers import OrganizationProfileSerializer, OrganizationLocationSerializer
from .serializers.users_serializers import OrganizationUsersSerializer, RegisterSerializer
from .serializers.roles_serializers import UserRoleSerializer, RolesFromOrganizationSerializer
from .serializers.invitations_serializer import InvitationSerializer
from .serializers.profile_serializers import ProfileSerializer

# from django.shortcuts import get_object_or_404

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    search_fields = ['user__username']
    # permission_classes = [CreateSuperUserPermission]

    def get_queryset(self):
        return Donation.objects.all()
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        user = self.request.query_params.get('email') or request.user.username
        donations = Donation.objects.filter(user__username=user)
        serializer = self.get_serializer(donations, many=True)
        return Response(serializer.data)

class OrganizationViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    # Define o serializer padrão para as outras operações
    def get_serializer_class(self):
        return OrganizationProfileSerializer

    def get_queryset(self):
        return OrganizationProfile.objects.all()

    # Resgata as organizações que o usuário faz parte
    @action(detail=False, methods=['get'])
    def user(self, request):
        user = request.user
        organizations = OrganizationProfile.objects.filter(organization__users=user)
        serializer = self.get_serializer(organizations, many=True)
        return Response(serializer.data)

    # Resgatar todos os dados da organização
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        organization = OrganizationProfile.objects.get(pk=pk)
        serializer = self.get_serializer(organization)
        return Response(serializer.data)
    
    # Resgatar todos os dados das organizações
    @action(detail=False, methods=['get'])
    def orgs_details(self, request):
        organization = OrganizationProfile.objects.all()
        serializer = self.get_serializer(organization, many=True)
        return Response(serializer.data)
    
    # Resgatar todos os usuários da organização
    @action(detail=True, methods=['get'])
    def all_users(self, request, pk=None):
        organization = OrganizationProfile.objects.get(pk=pk)
        users = organization.organization.users.all()
        serializer = OrganizationUsersSerializer(users, many=True)
        return Response(serializer.data)
    
    # Resgatar a localização das organizações
    @action(detail=False, methods=['get'])
    def location(self, request):
        organization = OrganizationProfile.objects.all()
        serializer = OrganizationLocationSerializer(organization, many=True)
        return Response(serializer.data)
    
    # Resgatar as doações da organização
    @action(detail=True, methods=['get'])
    def donations(self, request, pk=None):
        organization = OrganizationProfile.objects.get(pk=pk)
        donations = Donation.objects.filter(organization=organization.organization)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
    
    # Resgatar os usuários e as funções de cada usuário
    @action(detail=True, methods=['get'])
    def roles(self, request, pk=None):
        organization = OrganizationProfile.objects.get(pk=pk)
        roles = UserRole.objects.filter(organization=organization.organization)
        serializer = RolesFromOrganizationSerializer(roles, many=True)
        return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        user = self.request.query_params.get('email') or request.user.username
        profile = Profile.objects.get(user__username=user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

# Melhorar
class NotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Invitation.objects.all()
        
        # Filtrar as notificações do usuário
        user = self.request.user
        queryset = queryset.filter(invited_user=user)
        return queryset

# Melhorar
class UserRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = UserRole.objects.all()
        user = self.request.user
        
        # Filtrar as organizações do usuário
        if user is not None:
            queryset = queryset.filter(user=user)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        user = request.user
        user_roles = UserRole.objects.filter(user=user)
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer