from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Organization, OrganizationProfile

@receiver(post_save, sender=Organization)
def create_organization_profile(sender, instance, created, **kwargs):
    if created:
        OrganizationProfile.objects.create(organization=instance)

@receiver(post_save, sender=Organization)
def update_custom_users_organizations(sender, instance, created, **kwargs):
    if created:
        # Percorra todos os usuários associados à nova organização
        for user in instance.users.all():
            # Adicione a organização ao campo 'organizations' do usuário
            user.organizations.add(instance)

@receiver(m2m_changed, sender=Organization.users.through)
def update_custom_users_organizations_through(sender, instance, action, **kwargs):
    if action == 'post_add':
        # Percorra todos os usuários adicionados à organização
        for user_id in kwargs['pk_set']:
            # Recupere o usuário e a organização associada
            user = instance.users.filter(pk=user_id).first()
            # Adicione a organização ao campo 'organizations' do usuário
            if user:
                user.organizations.add(instance)
