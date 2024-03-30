from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from requests.exceptions import RequestException
from django.conf import settings
from organizations.models import Organization, OrganizationProfile
from users.models import CustomUser as User

import requests, json, googlemaps

# Create your views here.

def fetch_viacep_data(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'erro' in data and data['erro']:
            return JsonResponse({'error': 'CEP não existe'}, status=404) 
        return data
    except RequestException as e:
        print(f'Erro ao obter dados do CEP: {e}')
        return None

def get_cep(request, cep):
    cep = cep.replace('-', '')
    data = fetch_viacep_data(cep)
    
    if data is None:
        return JsonResponse({'error': 'CEP inválido'}, status=400)
    
    # Retornar a resposta JSON
    return JsonResponse(data, safe=False, status=200)

def home(request):
    return render(request, 'main/home.html')

def near_you(request):
    
    organizations = OrganizationProfile.objects.all()
    
    # Faço uma lista com as informações de todas as organizações, para que elas sejam inseridas no mapa de organizações próximas
    organizations_list = list(organizations.values_list('organization__name', 'organization__lat', 'organization__lng', 'organization__id', 'image'))
    organizations_list = [[item for item in sublist] for sublist in organizations_list]   
    
    context = {
        'key': settings.GOOGLE_API_KEY,
        'organizations': organizations_list
    }
    return render(request, 'main/near-you.html', context)

def donate(request):
    return render(request, 'main/donate.html')

def news(request):
    return render(request, 'main/news.html')

def news_detail(request):
    return render(request, 'main/news-detail.html')