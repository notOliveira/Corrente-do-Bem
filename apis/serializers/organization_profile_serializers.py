from rest_framework import serializers
from organizations.models import OrganizationProfile

from apis.serializers.organization_serializers import OrganizationSerializer, OrganizationGeolocationLatLonSerializer

# Serializer geral para o perfil da organização
class OrganizationProfileSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization', 'website', 'instagram']

    def get_organization(self, obj):
        # Verifica no contexto se a ação é "details" ou não
        request = self.context.get('request')
        if request and 'details' in request.resolver_match.url_name:
            # Retorna o serializer completo para detalhes
            return OrganizationSerializer(obj.organization).data
        # Retorna apenas o nome da organização (com StringRelatedField)
        return str(obj.organization)

# API de localização da organização (/near-you)
class OrganizationLocationSerializer(serializers.ModelSerializer):
    organization = OrganizationGeolocationLatLonSerializer()

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'organization', 'image']