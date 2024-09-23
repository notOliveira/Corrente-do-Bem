from rest_framework import serializers
from organizations.models import UserRole

from apis.serializers.users_serializers import OrganizationUsersSerializer
from apis.serializers.organization_serializers import OrganizationUserRolesSerializer

# Serializer geral para as funções dos usuários (/user-roles)
class UserRoleSerializer(serializers.ModelSerializer):
    user = OrganizationUsersSerializer()
    organization = OrganizationUserRolesSerializer()

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'organization', 'role']