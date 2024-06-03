from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomUser as User
from .models import Organization, OrganizationProfile, Donation, UserRole
from .forms import OrganizationCreationForm, OrganizationUpdateForm, OrganizationProfileUpdateForm, DonationForm
from django.conf import settings
import googlemaps

# Organizations

@login_required(login_url='login')
def organizations(request):
    orgs_profile = OrganizationProfile.objects.select_related('organization').filter(organization__users=request.user).order_by('organization__name')
    context = {
        'orgs': orgs_profile
    }
    return render(request, 'organizations/organizations.html', context)

@login_required(login_url='login')
def create_org(request):
    if request.method == "POST":
        form = OrganizationCreationForm(request.POST)
        if form.is_valid():
            try:
                organization = form.save(commit=False)
                organization.save()
                form.save_m2m()
                organization.users.add(request.user)

                UserRole.objects.create(user=request.user, organization=organization, role=0)
                
                # Adding the place_id, lat and lng to the organization
                address = f'{organization.street} {organization.number}, {organization.cep}, {organization.city} - {organization.state}'
                gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                location = gmap.geocode(address)[0]
    
                place_id = location.get('place_id', None)
                lat = location.get('geometry', {}).get('location', {}).get('lat', None)
                lng = location.get('geometry', {}).get('location', {}).get('lng', None)
                
                organization.lat = lat
                organization.lng = lng
                organization.place_id = place_id
                organization.save()
                                
                messages.success(request, 'Organização criada com sucesso!')
                
                return redirect('organizations')
            except Exception as e:
                print(e)
                messages.error(request, f'Houve um problema ao criar a organização. Por favor, tente novamente.')
                return redirect('create-org')
        else:
            email_errors = form.errors.get('email')
            if email_errors:
                messages.error(request, 'O email já está sendo utilizado por outra organização.')
            else:
                messages.error(request, 'Houve um problema ao validar o formulário. Por favor, tente novamente.')
            return redirect('create-org')
        
    return render(request, 'organizations/create-org.html')

def organization(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)

    user_role = None

    if request.user.is_authenticated:
        user_role = UserRole.objects.filter(user=request.user, organization=organization_profile.organization).first()
    
    location = [{
        'lat': float(organization_profile.organization.lat),
        'lng': float(organization_profile.organization.lng),
        'name' : organization_profile.organization.name
    }]
    
    context = {
        'org': organization_profile,
        'key': settings.GOOGLE_API_KEY,
        'location': location,
        'role': user_role.role if user_role else None,
        'role_name': user_role.get_role_display() if user_role else None
    }

    if not organization_profile.organization.users.filter(id=request.user.id).exists():
        return render(request, 'organizations/organization-view.html', context)

    return render(request, 'organizations/organization.html', context)

@login_required(login_url='login')
def settings_org(request, id):
    organization_profile = OrganizationProfile.objects.get(id=id)

    if request.user not in organization_profile.organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    organization = Organization.objects.get(id=id)
    user_role = UserRole.objects.filter(user=request.user, organization=organization_profile.organization).first()
    
    if not user_role.role == 0:
        messages.error(request, 'Você não tem permissão para acessar essa página')
        return redirect('organization', id=id)
    
    if request.method == "POST":        
        if 'edit-org' in request.POST:
            org_form = OrganizationUpdateForm(request.POST, instance=Organization.objects.filter(id=id).first())
            org_profile_form = OrganizationProfileUpdateForm(request.POST, request.FILES, instance=OrganizationProfile.objects.get(organization__id=id))
            if org_form.is_valid() and org_profile_form.is_valid():
                org_form.save()
                org_profile_form.save()
                
                organization = Organization.objects.get(id=id)
                
                address = f'{organization.street} {organization.number}, {organization.cep}, {organization.city} - {organization.state}'
                    
                # Adding the place_id, lat and lng to the organization
                gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                location = gmap.geocode(address)[0]

                place_id = location.get('place_id', None)
                lat = location.get('geometry', {}).get('location', {}).get('lat', None)
                lng = location.get('geometry', {}).get('location', {}).get('lng', None)
                
                organization.lat = lat
                organization.lng = lng
                organization.place_id = place_id
                organization.save()
                
                messages.success(request, 'Configurações atualizadas com sucesso!')
                return redirect('settings-org', id=id)
            else:
                messages.error(request, 'Erro ao atualizar as configurações. Por favor, corrija os erros abaixo.')
        
        elif 'delete-org' in request.POST:
            messages.success(request, 'Organização deletada com sucesso!')
            organization.delete()
            return redirect('organizations')
        
    categories = organization_profile.organization.category.all().values_list('name')
    
    org_categories = []
    
    for category in categories:
        org_categories.append(category[0])
    
    context = {
        'org' : organization,
        'org_profile': organization_profile,
        'categories': org_categories,
        'role': user_role.role,
        'current_org': {
            'id': organization_profile.organization.id,
            'name': organization_profile.organization.name
        }
    }
    return render(request, 'organizations/settings-org.html', context)

def users_org(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)
    
    if request.user not in organization_profile.organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    user_role = UserRole.objects.filter(user=request.user, organization=organization_profile.organization).first()
    
    if request.method == "POST":
        form = request.POST
        if 'leave-org' in form:

            # Se o usuário for colaborador, pode sair da organização

            if user_role.role == 1:
                UserRole.objects.filter(user=request.user, organization=organization_profile.organization).delete()
                Organization.objects.get(id=id).users.remove(request.user)
                request.user.organizations.remove(organization_profile.organization)
                messages.success(request, 'Você saiu da organização com sucesso.')
                return redirect('organizations')
            
            elif user_role.role == 0:
                if organization_profile.organization.users.count() == 1:
                    UserRole.objects.filter(user=request.user, organization=organization_profile.organization).delete()
                    Organization.objects.get(id=id).users.remove(request.user)
                    request.user.organizations.remove(organization_profile.organization)
                    messages.success(request, 'Você saiu da organização com sucesso.')
                    return redirect('organizations')
                # Validar se o usuário é o único administrador da organização
                elif UserRole.objects.filter(organization=organization_profile.organization, role=0).count() == 1:
                    messages.error(request, 'Você não pode sair da organização, pois é o único administrador.')
                    return redirect('users-org', id=id)
                else:
                    UserRole.objects.filter(user=request.user, organization=organization_profile.organization).delete()
                    Organization.objects.get(id=id).users.remove(request.user)
                    messages.success(request, 'Você saiu da organização com sucesso.')
                    return redirect('organizations')
        
        elif 'remove-user' in form:
            user_id = form.get('remove-user-input')
            # Remover usuário da organização
            try:
                organization_profile.organization.users.remove(User.objects.get(id=user_id))
                UserRole.objects.filter(user=User.objects.get(id=user_id), organization=organization_profile.organization).delete()
                User.objects.get(id=user_id).organizations.remove(organization_profile.organization)
                messages.success(request, 'Usuário removido com sucesso.')
                return redirect('users-org', id=id)
            except Exception as e:
                messages.error(request, 'Houve um problema ao remover o usuário.')
                return redirect('users-org', id=id)

        elif 'promote-user' in form:
            user_id = form.get('promote-user-input')
            # Promover usuário
            try:
                user = User.objects.get(username=user_id)
                user_role = UserRole.objects.filter(user=user, organization=organization_profile.organization).first()
                user_role.role = 0
                user_role.save()
                messages.success(request, 'Usuário promovido com sucesso.')
                return redirect('users-org', id=id)
            except Exception:
                messages.error(request, 'Houve um problema ao promover o usuário.')
                return redirect('users-org', id=id)

    users = organization_profile.organization.users.all()

    # Unir lista de usuários com seus respectivos roles
    users = [(user, UserRole.objects.filter(user=user, organization=organization_profile.organization).first().role) for user in users]
    
    context = {
        'org': organization_profile,
        'users': users,
        'role': user_role.role,
        'current_org': {
            'id': organization_profile.organization.id,
            'name': organization_profile.organization.name
        }
    }
    
    return render(request, 'organizations/organization-users.html', context)

# Donations

@login_required(login_url='login')
def org_donations(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)

    if request.user not in organization_profile.organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    user_role = UserRole.objects.filter(user=request.user, organization=organization_profile.organization).first()
        
    # Get last 10 donations
    donations = Donation.objects.filter(organization__id=id).order_by('-date')[:10]
    
    context = {
        'org': organization_profile,
        'donations': donations,
        'role': user_role.role,
        'current_org': {
            'id': organization_profile.organization.id,
            'name': organization_profile.organization.name
        }
    }
    
    return render(request, 'donations/org-donations.html', context)

@login_required(login_url='login')
def register_donation(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)
    
    if request.user not in organization_profile.organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES)
        email = request.POST.get('user')     
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('register-donation', id=id)
        
        if form.is_valid():
            donation = form.save(commit=False)
            donation.organization = organization_profile.organization
            donation.user = user
            donation.save()
            
            messages.success(request, 'Doação registrada com sucesso!')
            return redirect('org-donations', id=id)
        else:
            messages.error(request, 'Houve um problema ao registrar a doação. Por favor, tente novamente.')
            
            return redirect('register-donation', id=id)
    
    context = {
        'org': organization_profile,
        'current_org': {
            'id': organization_profile.organization.id,
            'name': organization_profile.organization.name
        }
    }
    
    return render(request, 'donations/register-donation.html', context)
