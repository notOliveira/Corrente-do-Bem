from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.models import CustomUser
from organizations.models import UserRole
from .forms import UserRegisterForm, ProfileUpdateForm, UsersUpdateForm

# Views

@login_required(login_url='/login')
def profile(request):
    if request.method == "POST":
        if 'delete-account' in request.POST:
            user_email = CustomUser.objects.filter(id=request.user.id).first()
    
            # Checando se o usuário é adminstrador único de alguma organizaçáo, caso seja, não poderá deletar a conta
            user_orgs = user_email.organizations.all()
            
            # Iterando sobre as organizações do usuário
            for org in user_orgs:
                # Verificando se o usuário é administrador ou colaborador
                user_role_org = UserRole.objects.filter(user=user_email, organization=org).first()
                # Caso seja colaborador, não haverá problemas em deixar a organização
                if user_role_org.role == 1:
                    continue
                # Caso não seja, será necessário verificar se o usuário é o único administrador da organização
                else:
                    # Criar uma variável que será usada para verificar se há mais de um administrador na organização
                    admin_validation = False
                    # Iterar sobre os usuários
                    for user in org.users.all():
                        # Caso o usuário seja o mesmo que está tentando deletar a conta, não será necessário verificar se ele é o único administrador
                        if user == user_email:
                            pass
                        else:
                            # Verificar a role dos usuários
                            user_role = UserRole.objects.filter(user=user, organization=org).first()
                            if user_role.role == 0:
                                admin_validation = True
                    
                    if admin_validation == False:
                        messages.error(request, f"Você é o único administrador da organização {org.name}. Por favor, adicione outro administrador antes de deletar a conta.")
                        return redirect('profile')
                    else:
                        continue
            
            subject = 'Encerramento de conta'
            email_template_name = 'delete_account.txt'
            parameters = {
                'username': user_email.first_name,
                'email': user_email.username,
                'site_name': 'Corrente do Bem',
            }
            email = render_to_string(email_template_name, parameters)
            try:
                send_mail(subject, email, '', [user_email.username], fail_silently=False)
            except Exception as e:
                print(e)
                return HttpResponse('Invalid Header')
            user_email.delete()
            messages.success(request, "Conta deletada com sucesso!")
            return redirect('home')
        
        elif 'save-profile' in request.POST:
                user_form = UsersUpdateForm(request.POST, instance=request.user)
                profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    messages.success(request, "Perfil atualizado com sucesso!")
                    return redirect('profile')

    user_form = UsersUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'users/profile.html', context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registro realizado com sucesso!')
                return redirect('home')
            else:
                messages.error(request, 'Houve um problema ao criar o usuário. Por favor, tente novamente.')
        else:
            errors = form.errors.as_data()
            if 'email' in errors:
                messages.error(request, 'O email já está cadastrado.')
            elif 'password2' in errors:
                messages.error(request, 'As senhas não coincidem ou a senha é fraca.')
            else:
                messages.error(request, 'Por favor, preencha os campos corretamente.')

    return render(request, 'users/register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.filter(email=email.lower()).first()
        user_instance = authenticate(request, email=email.lower(), password=password)
        
        if not user:
            messages.error(request, "Usuário com esse email não existe! Por favor tente novamente.")
            return redirect('login')
        elif user_instance is None:
            messages.error(request, "Senha incorreta! Por favor tente novamente.")
            return redirect('login')
        else:
            login(request, user_instance)
            return redirect('home')
    
    return render(request, 'users/login.html')

def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = CustomUser.objects.filter(Q(username=data)).first()
            if user_email is None:
                messages.error(request, 'Email não encontrado!')
                return redirect('reset-password')
            elif user_email is not None:
                subject = 'Redefinição de senha'
                email_template_name = 'reset_password_email.txt'
                parameters = {
                    'username': user_email.first_name,
                    'email': user_email.username,
                    'domain': request.get_host(),
                    'site_name': 'Corrente do Bem',
                    'uid': urlsafe_base64_encode(force_bytes(user_email.pk)),
                    'token': default_token_generator.make_token(user_email),
                    'protocol': request.scheme,
                }
                email = render_to_string(email_template_name, parameters)
                
                try:
                    send_mail(subject, email, '', [user_email.username], fail_silently=False)
                except Exception as e:
                    print(e)
                    return HttpResponse('Invalid Header')
                messages.success(request, 'Um email foi enviado para você com instruções para redefinir sua senha.')
                return redirect('home')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form  
    }
    return render(request, 'users/reset-password.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso!")
    return redirect('home')