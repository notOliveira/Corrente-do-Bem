# Views, viewsets e generics da aplicação apis
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import CreateSuperUserPermission
# Models
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

class NotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Invitation.objects.all()
        
        user = self.request.user
        
        if not user.is_superuser:
            return queryset.filter(invited_user=user)
        
        # Adicionando filtros
        organization = self.request.query_params.get('organization')
        if organization is not None:
            queryset = queryset.filter(organization__name=organization)        

        invited_user = self.request.query_params.get('invited_user')
        if invited_user is not None:
            queryset = queryset.filter(invited_user__username=invited_user)

        invited_by = self.request.query_params.get('invited_by')
        if invited_by is not None:
            queryset = queryset.filter(invited_by__username=invited_by)

        return queryset
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        user = request.user
        notifications = Invitation.objects.filter(invited_user=user)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    # Deletar convite
    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        try:
            invitation = Invitation.objects.get(pk=pk)
            
            # Verifica se o usuário que está tentando apagar o convite é:
            # - Superusuário 
            # - Usuário convidado
            # - Quem convidou
            # Caso seja, ele pode apagar o convite
            if not (request.user.is_superuser or 
                    invitation.invited_user == request.user or 
                    invitation.invited_by == request.user):
                return Response({'error': 'Você não tem permissão para remover esse convite.'}, status=403)
            
            # Deleta o convite
            invitation.delete()
            return Response({'message': 'Convite removido.'}, status=204)
        
        except Invitation.DoesNotExist:
            return Response({'error': 'Convite não encontrado.'}, status=404)

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