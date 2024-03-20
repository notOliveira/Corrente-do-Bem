from django import forms
from .models import Organization, OrganizationProfile

class OrganizationCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'phone', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description', 'category']
        
class OrganizationUpdateForm(forms.ModelForm):
            
    class Meta:
        model = Organization
        fields = ['name', 'category', 'phone', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description']

class OrganizationProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['image', 'website', 'instagram']
        