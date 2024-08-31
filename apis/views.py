from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from organizations.models import Donation, OrganizationProfile
from .permissions import CreateSuperUserPermission
from .serializers import DonationSerializer, OrganizationProfileSerializer

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [CreateSuperUserPermission]
    search_fields = ['user__username']

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

# Organizations that the user is part of
class OrganizationProfileViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return OrganizationProfile.objects.filter(organization__users=user)

    @action(detail=False, methods=['get'])
    def current_user_organizations(self, request):
        user = request.user
        organizations = OrganizationProfile.objects.filter(organization__users=user)
        serializer = self.get_serializer(organizations, many=True)
        return Response(serializer.data)