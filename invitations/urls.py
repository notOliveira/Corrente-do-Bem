from django.urls import path
from . import views

urlpatterns = [
    path('<int:organization_id>/invite/', views.invite_users, name='invite-users'),
    path('accept-invite/<str:token>/', views.accept_invite, name='accept-invite'),
    path('invites/', views.invites, name='invites'),
]