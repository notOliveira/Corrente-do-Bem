from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


r = DefaultRouter()

r.register(r"donations", views.DonationsViewSet, basename='api-donations')
r.register(r"organizations", views.OrganizationProfileViewSet, basename='api-organizations')

urlpatterns = [
    # DefaultRouter
    path('', include(r.urls), name='api'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]