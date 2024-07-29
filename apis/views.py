from django.shortcuts import render
from rest_framework import viewsets
from organizations.models import Donation
from .permissions import CreateSuperUserPermission
from .serializers import DonationSerializer

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [CreateSuperUserPermission]