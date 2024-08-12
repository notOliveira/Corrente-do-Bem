from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Invitation(models.Model):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    invited_user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    invited_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='invited_by')
    invite_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'Convite - {self.invited_user.username} - {self.organization.name}'