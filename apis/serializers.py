from rest_framework import serializers
from organizations.models import Donation
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class DonationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Donation
        fields = ['id', 'user', 'date', 'organization']