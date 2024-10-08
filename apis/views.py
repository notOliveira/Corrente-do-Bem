from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from organizations.models import Donation, OrganizationProfile, UserRole
from users.models import Profile
from invitations.models import Invitation
from .serializers import DonationSerializer, OrganizationProfileDetailSerializer, OrganizationProfileBasicSerializer, ProfileSerializer, InvitationSerializer, OrganizationUsersSerializer, UserRoleSerializer
# from django.shortcuts import get_object_or_404
# from .permissions import CreateSuperUserPermission

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    search_fields = ['user__username']
    # permission_classes = [CreateSuperUserPermission]

    def get_queryset(self):
        queryset = Donation.objects.all()

        # Filters
        organization_id = self.request.query_params.get('organization_id')
        user_email = self.request.query_params.get('user_email')

        if organization_id is not None:
            queryset = queryset.filter(organization__id=organization_id)
        if user_email is not None:
            queryset = queryset.filter(user__email=f'{user_email}')
        
        return queryset

class OrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # Define o serializer padrão para as outras operações
    def get_serializer_class(self):
        if 'details' in self.action:
            return OrganizationProfileDetailSerializer
        return OrganizationProfileBasicSerializer

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
    def users(self, request, pk=None):
        organization = OrganizationProfile.objects.get(pk=pk)
        users = organization.organization.users.all()
        serializer = OrganizationUsersSerializer(users, many=True)
        return Response(serializer.data)
    
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()

        # Filters
        email = self.request.query_params.get('email')

        if email is not None:
            queryset = queryset.filter(email=f'{email}')
        
        return queryset

class NotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Invitation.objects.all()
        
        # Filtrar as notificações do usuário
        user = self.request.user
        queryset = queryset.filter(invited_user=user)
        return queryset

class UserRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

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