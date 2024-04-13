from django.shortcuts import redirect, get_object_or_404, render
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from organizations.models import Organization, OrganizationProfile, UserRole
from users.models import CustomUser as User
from .models import Invitation

def invite_users(request, organization_id):
    organization_profile = OrganizationProfile.objects.get(organization__id=organization_id)
    
    if request.user not in organization_profile.organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    user_role = UserRole.objects.filter(user=request.user, organization=organization_profile.organization).first()
    
    if not user_role.role == 0:
        messages.error(request, 'Você não tem permissão para acessar essa página')
        return redirect('organization', id=organization_id)
    
    
    if request.method == 'POST':
        invited_user = User.objects.get(username=request.POST.get('email'))

        # Verifique se já existe um convite pendente para este usuário nesta organização
        if Invitation.objects.filter(organization=organization_profile.organization, invited_user=invited_user, is_accepted=False).exists():
            messages.error(request, f'O usuário {invited_user.first} foi convidado para se juntar a esta organização.')
            return 

        # Crie um novo convite
        invitation = Invitation.objects.create(organization=organization_profile.organization, invited_user=invited_user)

        # Envie o email de convite
        subject = 'Convite para se juntar à organização'
        email_template_name = 'invite_org.txt'
        parameters = {
            'username': invited_user.first_name,
            'email': invited_user.email,
            'domain': 'localhost:8000',
            'site_name': 'Zero Fome',
            'token': invitation.token,
            'protocol': 'http'
        }
        email = render_to_string(email_template_name, parameters)
        
        send_mail(subject, email, '', [invitation.invited_user.username], fail_silently=False)

        return redirect('invitation_sent_page')  # Redirecionar para uma página informando que o convite foi enviado
    
    return render(request, 'invitations/invite-users.html')

def accept_invitation(request, token):
    invitation = get_object_or_404(Invitation, token=token)

    # Marque o convite como aceito
    invitation.is_accepted = True
    invitation.save()

    # Adicione o usuário à organização
    invitation.organization.users.add(invitation.invited_user)

    return redirect('invitation_accepted_page')  # Redirecionar para uma página informando que o convite foi aceito