from django.urls import path
from . import views

urlpatterns = [
    path('<int:organization_id>/invite/', views.invite_users, name='invite-users'),   
]