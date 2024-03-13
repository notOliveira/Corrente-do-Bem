from django.urls import path
from . import views as org_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', org_views.organizations, name='organizations'),
    path('create/', org_views.create_org, name='create-org'),
    path('<int:id>/', org_views.organization, name='organization'),
    path('<int:id>/settings/', org_views.settings_org, name='settings-org')
]