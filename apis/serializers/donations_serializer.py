from rest_framework import serializers
from organizations.models import Donation

from apis.serializers.users_serializers import UserProfileSerializer

# Serializer geral para as doações
class DonationSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Donation
        fields = ['id', 'user', 'date', 'organization', 'image']