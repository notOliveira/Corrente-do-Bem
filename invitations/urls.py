from django.urls import path
from . import views

urlpatterns = [
    path('organizations/<int:organization_id>/invite/', views.invite_users, name='invite-users'),
    path('organizations/accept-invite/<str:token>/', views.accept_invite, name='accept-invite'),
    path('organizations/decline-invite/<str:token>/', views.accept_invite, name='decline-invite'),
    path('invites/', views.invites, name='invites'),
]