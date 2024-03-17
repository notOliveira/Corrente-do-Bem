from django import forms
from .models import Organization, OrganizationProfile

class OrganizationCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        # fields = ['name', 'email', 'category', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description']
        fields = '__all__'
        
        # add form-control in fields
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class OrganizationUpdateForm(forms.ModelForm):
            
    class Meta:
        model = Organization
        fields = ['name', 'category', 'phone', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description']

class OrganizationProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['image', 'website', 'instagram']
        