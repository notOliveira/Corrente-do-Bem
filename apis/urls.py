from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

r = DefaultRouter()

r.register(r"donations", views.DonationsViewSet, basename='api-donations')

urlpatterns = [
    # DefaultRouter
    path('', include(r.urls), name='api'),
]