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
        fields = ['user', 'organization', 'role']

# Serializer para resgatar as funções dos usuários de uma organização, com o código e nome da função (/organization/<id>/roles)
class RolesFromOrganizationSerializer(serializers.ModelSerializer):
    user = OrganizationUsersSerializer()
    # get_role_name = lambda self, obj: obj.get_role_display()
    # role_name = serializers.SerializerMethodField('get_role_name')

    class Meta:
        model = UserRole
        fields = ['user', 'role']