from rest_framework import serializers
from users.models import Profile

from apis.serializers.users_serializers import UserProfileSerializer

# Serializer geral para os perfis dos usuários
class ProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']