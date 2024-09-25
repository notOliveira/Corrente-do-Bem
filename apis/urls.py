from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView
from . import views


r = DefaultRouter()

r.register(r"donations", views.DonationsViewSet, basename='api-donations')
r.register(r"organizations", views.OrganizationViewSet, basename='api-organizations')
r.register(r"profiles", views.ProfileViewSet, basename='api-profiles')
r.register(r"notifications", views.NotificationsViewSet, basename='api-notifications')
r.register(r"user-roles", views.UserRoleViewSet, basename='api-user-roles')

urlpatterns = [
    # DefaultRouter
    path('', include(r.urls), name='api'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]