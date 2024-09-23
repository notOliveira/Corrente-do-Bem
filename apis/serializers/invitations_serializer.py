
from rest_framework import serializers
from invitations.models import Invitation

# Serializer geral para os convites
class InvitationSerializer(serializers.ModelSerializer):
    invited_by = serializers.StringRelatedField()
    organization = serializers.StringRelatedField()
    invite_date = serializers.DateTimeField(format='%d/%m/%Y - %H:%M:%S')

    class Meta:
        model = Invitation
        fields = '__all__'