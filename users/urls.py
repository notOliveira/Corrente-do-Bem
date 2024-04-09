from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', user_views.login_user, name='login'),
    path('logout/', user_views.logout_user, name='logout'),
    path('register/', user_views.register_user, name='register'),
    path('profile/', user_views.profile, name='profile'),
    # Solicitação de reset
    path('reset_password/', user_views.password_reset_request, name="reset-password"),
    # Confirmação da solicitação de reset de senha
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password-reset-sent.html'), name='password_reset_done'),
    # Reset de senha
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html'), name='password_reset_confirm'),
    # Confirmação do reset de senha
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password-reset-complete.html'), name='password_reset_complete'),
]