from django import forms
from .models import Organization, OrganizationProfile

class OrganizationCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        
class OrganizationUpdateForm(forms.ModelForm):
            
    class Meta:
        model = Organization
        fields = ['name', 'category', 'phone', 'cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement', 'description']

class OrganizationProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['image', 'website', 'instagram']
        