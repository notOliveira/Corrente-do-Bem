from rest_framework import serializers
from users.models import CustomUser

# Serializer geral para os usuários
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# Serializer com campos do perfil do usuário
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'cep', 'first_name', 'last_name']

# Serializer com campos básicos do usuário
class OrganizationUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']