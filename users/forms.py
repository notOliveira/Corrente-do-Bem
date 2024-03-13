from django import forms
from .models import CustomUser as User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'cep', 'first_name', 'last_name']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Defina o username como o email
        if commit:
            user.save()
        return user
        
class UsersUpdateForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = ['cep', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']