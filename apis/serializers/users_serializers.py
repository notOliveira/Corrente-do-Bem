from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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

# Serializer para registro de usuário
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    cep = serializers.CharField(max_length=9, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'cep', 'first_name', 'last_name', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password': 'As senhas não coincidem.'})
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['username'],
            cep=validated_data.get('cep', None),
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None)
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    
    
