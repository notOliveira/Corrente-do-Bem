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

# Serializer básico para respostas simples (sem todos os dados da Organization)
class OrganizationProfileBasicSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    id = OrganizationSerializer().fields['id']

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization', 'website', 'instagram']

# Serializer detalhado para respostas que incluem todos os dados da Organization
class OrganizationProfileDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization', 'website', 'instagram']