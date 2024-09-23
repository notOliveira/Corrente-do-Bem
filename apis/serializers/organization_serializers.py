from rest_framework import serializers
from organizations.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationUserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

class OrganizationGeolocationLatLonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['lat', 'lng']

# API de localização da organização (/near-you)
class OrganizationLocationSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'latitude', 'longitude']

    def get_organization(self, obj):
        return str(obj.organization)