from rest_framework import serializers
from organizations.models import Donation, OrganizationProfile, Organization
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']

class DonationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Donation
        fields = ['id', 'user', 'date', 'organization']

class OrganizationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization']

class OrganizationSerializer(serializers.ModelSerializer):
    profile = OrganizationProfileSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'phone', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'place_id', 'lat', 'lng', 'description', 'profile']