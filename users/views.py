from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UsersUpdateForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from users.models import CustomUser
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

@login_required(login_url='/login')
def profile(request):
    if request.method == "POST":
        user_form = UsersUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profile')
    else:
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
        user_instance = authenticate(request, email=email.lower(), password=password)
        
        if user_instance is not None:
            login(request, user_instance)
            return redirect('home')
        else:
            messages.error(request, "Usuário não existe! Por favor tente novamente.")
            return redirect('login')
    else:
        messages.error(request, '')
        return render(request, 'users/login.html', {})

def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = CustomUser.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Redefinição de senha'
                    email_template_name = 'users/reset_password_email.txt'
                    parameters = {
                        'username': user.username,
                        'email': user.email,
                        # Mudar para domínio de produção
                        'domain': 'localhost:8000',
                        'site_name': 'Zero Fome',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form  
    }
    return render(request, 'users/password_reset.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso!")
    return redirect('home')