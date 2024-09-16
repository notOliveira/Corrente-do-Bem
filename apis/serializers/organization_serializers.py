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