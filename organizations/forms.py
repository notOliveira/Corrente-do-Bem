from django import forms
from .models import Organization, OrganizationProfile

class OrganizationCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description']
        dictionary = {}
        for field in fields:
            dictionary[field] = forms.TextInput(attrs={'class': 'form-control'})
        widgets = dictionary
        labels = {
            'name': 'Nome',
            'email': 'Email',
            'cep': 'CEP',
            'street': 'Rua',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
            'number': 'Número',
            'complement': 'Complemento',
            'description': 'Descrição',
        }
        
class OrganizationUpdateForm(forms.ModelForm):
            
    class Meta:
        model = Organization
        fields = ['name', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description']

class OrganizationProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['image']
        