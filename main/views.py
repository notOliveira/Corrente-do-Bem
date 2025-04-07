from django.shortcuts import render
from django.http import JsonResponse
from requests.exceptions import RequestException
from django.conf import settings
from organizations.models import OrganizationProfile, Donation
import requests

# Create your views here.

def home(request):
    context = {
        'total_donations': Donation.objects.count()
    }
    return render(request, 'main/home.html', context)

def near_you(request):
    
    organizations = OrganizationProfile.objects.all()
    
    # Faço uma lista com as informações de todas as organizações, para que elas sejam inseridas no mapa de organizações próximas
    organizations_list = list(organizations.values_list('organization__name', 'organization__lat', 'organization__lng', 'organization__id', 'image'))
    organizations_list = [[item for item in sublist] for sublist in organizations_list] 
    
    context = {
        'organizations': organizations_list
    }
    return render(request, 'main/near-you.html', context)

def error_404(request):
    return render(request, 'main/404.html')

# def donate(request):
#     return render(request, 'main/donate.html')

# def news(request):
#     return render(request, 'main/news.html')

# def news_detail(request):
#     return render(request, 'main/news-detail.html')