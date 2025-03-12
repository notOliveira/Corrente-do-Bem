import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Verifica se a API URL está configurada corretamente
if not settings.HERE_API_URL:
    raise ImproperlyConfigured("HERE_API_URL não está definido nas configurações.")

def save_coordinates_here(organization):
    """ Obtém latitude e longitude de uma organização usando a API Here Maps. """

    # Monta o endereço formatado
    address = f"{organization.street}, {organization.number}, {organization.cep} - {organization.city}"
    url = f"{settings.HERE_API_URL}&q={address}"

    try:
        response = requests.get(url, timeout=5)  # Timeout evita espera infinita
        response.raise_for_status()  # Lança erro se a requisição falhar

        data = response.json()
        items = data.get("items", [])

        if not items:
            print(f'Endereço não encontrado: "{address}".')
            return None, None  # Retorna valores explícitos

        item = items[0]
        position = item.get("position", {})

        lat = position.get("lat")
        lng = position.get("lng")

        if lat is None or lng is None:
            print(f'Coordenadas não encontradas para: "{address}".')
            return None, None

        print(f"Endereço solicitado: {address}")
        print(f"Endereço encontrado: {item.get('title', 'Desconhecido')}")
        print(f"{lat} {lng}\n")

        # Atualiza o objeto e salva
        organization.lat = lat
        organization.lng = lng
        organization.save()

        return lat, lng  # Retorna valores para possível uso futuro

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar coordenadas: {e}")
        return None, None