from rest_framework import serializers
from organizations.models import Donation, OrganizationProfile, Organization
from users.models import CustomUser, Profile
from invitations.models import Invitation

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'cep', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']

class DonationSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Donation
        fields = ['id', 'user', 'date', 'organization']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationProfileBasicSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    id = OrganizationSerializer().fields['id']

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization', 'website', 'instagram']

class OrganizationProfileDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = OrganizationProfile
        fields = ['id', 'image', 'organization', 'website', 'instagram']

class InvitationSerializer(serializers.ModelSerializer):
    invited_by = serializers.StringRelatedField()
    organization = serializers.StringRelatedField()
    invite_date = serializers.DateTimeField(format='%d/%m/%Y - %H:%M:%S')

    class Meta:
        model = Invitation
        fields = '__all__'