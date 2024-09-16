from rest_framework import serializers
from organizations.models import UserRole
# Serializers
from apis.serializers.users_serializers import UserProfileSerializer
from apis.serializers.organization_serializers import OrganizationUserRolesSerializer

class UserRoleSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    organization = OrganizationUserRolesSerializer()

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'organization', 'role']