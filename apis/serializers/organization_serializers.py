from rest_framework import serializers
from organizations.models import Organization

# Serializer geral para as organizações
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

# Serializer para o campo "organization" do serializer geral de user roles
class OrganizationUserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

# Serializer para a o campo de 'organization' da API de localização da organização
class OrganizationGeolocationLatLonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['lat', 'lng']