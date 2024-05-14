from invitations.models import Invitation

def global_variables(request):
    # Defina suas variáveis globais aqui
    return {
        'notifications': True if request.user.is_authenticated and Invitation.objects.filter(invited_user=request.user, is_accepted=False).exists() else False
    }