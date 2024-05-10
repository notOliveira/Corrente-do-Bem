from django.shortcuts import redirect, get_object_or_404, render
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError
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
        
        for email_user in list(request.POST.getlist('email')):
            try:
                invited_user = User.objects.filter(username=email_user).first()
                
                if not invited_user:
                    raise Exception(f'O usuário com email {email_user} não foi encontrado.')
                
                # Verificar se o usuário já pertence à organização
                if invited_user in organization_profile.organization.users.all():
                    messages.info(request, f'O usuário {invited_user.first_name} já faz parte desta organização.')
                    continue
                # Verifique se já existe um convite pendente para este usuário nesta organização
                elif Invitation.objects.filter(organization=organization_profile.organization, invited_user=invited_user, is_accepted=False).exists():
                    messages.error(request, f'O usuário {invited_user.first_name} já foi convidado para se juntar a esta organização.')
                    continue

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
                    'protocol': 'http',
                    'org_name': invitation.organization.name
                }
                email = render_to_string(email_template_name, parameters)
                
                send_mail(subject, email, '', [invitation.invited_user.username], fail_silently=False)
                
                messages.success(request, f"Um convite foi enviado para {parameters['email']}.")
                
            except Exception as e:
                messages.error(request, e)
                continue
        
        return redirect('organization', id=organization_id) 
    
    return render(request, 'invitations/invite-users.html', {'id': organization_profile.organization.id})

def accept_invite(request, token):
    try:
        invitation = Invitation.objects.get(token=token)
    except ValidationError:
        messages.error(request, 'Este convite é inválido, expirou ou já foi aceito.')
        return redirect('organizations')
    except Invitation.DoesNotExist:
        messages.error(request, 'Este convite é inválido, expirou ou já foi aceito.')
        return redirect('organizations')
    
    # Validar se o usuário logado é o mesmo da solicitação. Caso não seja, mostre uma mensagem de erro
    if not request.user == invitation.invited_user:
        messages.error(request, 'Você não tem permissão para aceitar este convite.')
        return redirect('organizations')
    
    # Adicione o usuário à organização
    invitation.organization.users.add(invitation.invited_user)
    
    # Adicionando usuário como colaborador
    UserRole.objects.create(user=invitation.invited_user, organization=invitation.organization, role=1)
    
    invitation.delete()
    
    messages.success(request, f'Você aceitou o convite para se juntar à organização {invitation.organization.name}.')

    return redirect('organizations')