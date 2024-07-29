from rest_framework import viewsets
from organizations.models import Donation
from .permissions import CreateSuperUserPermission
from .serializers import DonationSerializer

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [CreateSuperUserPermission]

    def get_queryset(self):
        queryset = Donation.objects.all()

        # Filters
        organization_id = self.request.query_params.get('organization_id')

        if organization_id is not None:
            queryset = queryset.filter(organization__id=organization_id)
        return queryset