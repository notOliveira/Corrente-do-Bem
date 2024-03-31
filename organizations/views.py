from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomUser as User
from .models import Organization, OrganizationProfile, Donation
from .forms import OrganizationCreationForm, OrganizationUpdateForm, OrganizationProfileUpdateForm, DonationForm
from django.conf import settings
import googlemaps

# Organizations

@login_required(login_url='/login')
def organizations(request):
    orgs_profile = OrganizationProfile.objects.select_related('organization').filter(organization__users=request.user)
    context = {
        'orgs': orgs_profile
    }
    return render(request, 'organizations/organizations.html', context)

@login_required(login_url='/login')
def create_org(request):
    if request.method == "POST":
        form = OrganizationCreationForm(request.POST)
        if form.is_valid():
            try:
                organization = form.save(commit=False)
                organization.save()
                form.save_m2m()
                organization.users.add(request.user)
                
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
    
    location = [{
        'lat': float(organization_profile.organization.lat),
        'lng': float(organization_profile.organization.lng),
        'name' : organization_profile.organization.name
    }]
    
    context = {
        'org': organization_profile,
        'key': settings.GOOGLE_API_KEY,
        'location': location
    }

    if not organization_profile.organization.users.filter(id=request.user.id).exists():
        return render(request, 'organizations/organization-view.html', context)

    return render(request, 'organizations/organization.html', context)

def settings_org(request, id):
    if request.method == "POST":
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
    
    organization = Organization.objects.get(id=id)
    
    categories = organization.category.all().values_list('name')
    
    org_categories = []
    
    for category in categories:
        org_categories.append(category[0])
    
    if request.user not in organization.users.all():
        messages.error(request, 'Você não tem permissão para acessar essa organização.')
        return redirect('organizations')
    
    organization_profile = OrganizationProfile.objects.get(organization=organization)
    
    context = {
        'org' : organization,
        'org_profile': organization_profile,
        'categories': org_categories
    }
    return render(request, 'organizations/settings-org.html', context)

# Donations

def org_donations(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)
    # Get last 10 donations
    donations = Donation.objects.filter(organization__id=id).order_by('-date')[:10]
    
    context = {
        'org': organization_profile,
        'donations': donations
    }
    
    return render(request, 'donations/org-donations.html', context)

def register_donation(request, id):
    organization_profile = get_object_or_404(OrganizationProfile, organization__id=id)
    
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
        'org': organization_profile
    }
    
    return render(request, 'donations/register-donation.html', context)

