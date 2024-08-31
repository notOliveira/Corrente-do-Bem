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


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationProfileSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer().fields['name']
    id = OrganizationSerializer().fields['id']

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization', 'website', 'instagram']