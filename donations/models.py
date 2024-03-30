from django.db import models
from users.models import CustomUser as User
from organizations.models import Organization

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    def upload_to_directory(instance, filename):
        # Defina o caminho de upload com base no ID da organização
        return f'donations/{instance.organization_id}/{filename}'

    image = models.ImageField(upload_to=upload_to_directory, blank=True, null=True)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

