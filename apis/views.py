from rest_framework import viewsets
from organizations.models import Donation
from .permissions import CreateSuperUserPermission
from .serializers import DonationSerializer

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