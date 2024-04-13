from django.urls import path
from . import views

urlpatterns = [
    
    # Organizations
    path('', views.organizations, name='organizations'),
    path('create/', views.create_org, name='create-org'),
    path('<int:id>/', views.organization, name='organization'),
    path('<int:id>/settings/', views.settings_org, name='settings-org'),
    
    # Donations
    path('<int:id>/donations/', views.org_donations, name='org-donations'),
    path('<int:id>/donations/new', views.register_donation, name='register-donation'),
]