from django.shortcuts import redirect, get_object_or_404, render
from django.db import transaction
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from organizations.models import OrganizationProfile, UserRole
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
                
                if invited_user in organization_profile.organization.users.all():
                    messages.info(request, f'O usuário {invited_user.first_name} já faz parte desta organização.')
                    continue
                elif Invitation.objects.filter(organization=organization_profile.organization, invited_user=invited_user).exists():
                    messages.error(request, f'O usuário {invited_user.first_name} já foi convidado para se juntar a esta organização.')
                    continue
                
                with transaction.atomic():
                    invitation = Invitation.objects.create(organization=organization_profile.organization, invited_user=invited_user, invited_by=request.user)

                    subject = 'Convite para se juntar à organização'
                    email_template_name = 'invite_org.html'
                    parameters = {
                        'username': invited_user.first_name,
                        'email': invited_user.email,
                        'domain': 'localhost:8000',
                        'site_name': 'Corrente do Bem',
                        'token': invitation.token,
                        'protocol': 'http',
                        'org_name': invitation.organization.name
                    }
                    
                    html_content = render_to_string(email_template_name, parameters)
                    text_content = strip_tags(html_content)
                    
                    email = EmailMultiAlternatives(subject, text_content, '', [invited_user.email])
                    email.attach_alternative(html_content, "text/html")
                    
                    email.send()
                
                messages.success(request, f"Um convite foi enviado para {parameters['email']}.")
                
            except Exception as e:
                messages.error(request, e)
                continue
        
        return redirect('organization', id=organization_id) 
    
    context = {
        'current_org': {
            'id': organization_profile.organization.id,
            'name': organization_profile.organization.name
        }
    }
    return render(request, 'invitations/invite-users.html', context)

def accept_invite(request, token):
    referer = request.META.get('HTTP_REFERER') or 'organizations'
    try:
        invitation = Invitation.objects.get(token=token)
    except ValidationError:
        messages.error(request, 'Este convite é inválido, expirou ou já foi aceito.')
        return redirect(referer)
    except Invitation.DoesNotExist:
        messages.error(request, 'Este convite é inválido, expirou ou já foi aceito.')
        return redirect(referer)
    
    # Validar se o usuário logado é o mesmo da solicitação. Caso não seja, mostre uma mensagem de erro
    if not request.user == invitation.invited_user:
        messages.error(request, 'Você não tem permissão para aceitar este convite.')
        return redirect(referer)
    
    # Adicione o usuário à organização
    invitation.organization.users.add(invitation.invited_user)
    
    # Adicionando usuário como colaborador
    UserRole.objects.create(user=invitation.invited_user, organization=invitation.organization, role=1)
    
    invitation.delete()
    
    messages.success(request, f'Você aceitou o convite para se juntar à organização {invitation.organization.name}.')

    return redirect(referer)

def decline_invite(request, token):

    referer = request.META.get('HTTP_REFERER') or 'organizations'
    try:
        invitation = Invitation.objects.get(token=token)
    except ValidationError:
        messages.error(request, 'Este convite é inválido, expirou ou já foi aceito.')
        return redirect(referer)
    except Invitation.DoesNotExist:
        messages.error(request, 'Este convite é inválido, expirou ou já foi aceito.')
        return redirect(referer)
    
    # Validar se o usuário logado é o mesmo da solicitação. Caso não seja, mostre uma mensagem de erro
    if not request.user == invitation.invited_user:
        messages.error(request, 'Você não tem permissão para rejeitar este convite.')
        return redirect(referer)
    
    # Remover o convite
    invitation.delete()
    
    messages.success(request, f'Você rejeitou o convite para se juntar à organização {invitation.organization.name}.')

    return redirect(referer)

def invites(request):
    user_invites = Invitation.objects.filter(invited_user=request.user)
    
    if request.method == 'POST':
        if 'decline-invite' in request.POST:
            invite_id = request.POST.get('decline-invite-input')
            token = get_object_or_404(Invitation, id=invite_id).token
            return decline_invite(request, token)
        
        return redirect('invites')
    context = {
        'invites': user_invites
    }
    return render(request, 'invitations/invites.html', context)
