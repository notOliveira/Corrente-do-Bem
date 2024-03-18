from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Organization, OrganizationProfile
from .forms import OrganizationCreationForm, OrganizationUpdateForm, OrganizationProfileUpdateForm

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
    
    context = {
        'org': organization_profile
    }

    if not organization_profile.organization.users.filter(id=request.user.id).exists():
        return render(request, 'organizations/organization-view.html', context)

    context = {
        'org': organization_profile
    }
    return render(request, 'organizations/organization.html', context)

def settings_org(request, id):
    if request.method == "POST":
        org_form = OrganizationUpdateForm(request.POST, instance=Organization.objects.filter(id=id).first())
        org_profile_form = OrganizationProfileUpdateForm(request.POST, request.FILES, instance=OrganizationProfile.objects.get(organization__id=id))
        if org_form.is_valid() and org_profile_form.is_valid():
            org_form.save()
            org_profile_form.save()
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
