from django.core.management.base import BaseCommand
from users.models import CustomUser
from django.conf import settings
from organizations.models import Organization, Category, UserRole
from organizations.constants import CATEGORY_CHOICES
import googlemaps

class Command(BaseCommand):
    help = 'Cria os objetos padrão do banco'

    def handle(self, *args, **options):

        try: 
            # Adiciona as categorias
            Category.objects.bulk_create([Category(name=value) for value, _ in CATEGORY_CHOICES if not Category.objects.filter(name=value).exists()])
            
            # Criando superusuário
            admin_email = 'admin@admin.com'
            if not CustomUser.objects.filter(email=admin_email).exists():
                CustomUser.objects.create_superuser(
                    email=admin_email,
                    username=admin_email,
                    first_name='Admin',
                    last_name='Administrator',
                    password='admin'
                )

            # Criando organizações
            orgs = [
                {
                    'name': 'Organização 1',
                    'email': 'org1@email.com',
                    'phone': '11968317891',
                    'cep': '04458-140',
                    'street': 'Rua Pedro Germi',
                    'neighborhood': 'Jardim Sônia',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '38',
                    'description': 'Descrição da organização 1',
                    'category_name': 1,
                    'complement': ''
                },
                {
                    'name': 'Organização 2',
                    'email': 'org2@email.com',
                    'phone': '11968317891',
                    'cep': '65912-300',
                    'street': 'Rua Mamoré',
                    'neighborhood': 'Parque Santa Lúcia',
                    'city': 'Imperatriz',
                    'state': 'MA',
                    'number': '193',
                    'description': 'Descrição da organização',
                    'category_name': 2,
                    'complement': ''
                },
                {
                    'name': 'Organização 3',
                    'email': 'org3@email.com',
                    'phone': '11968317891',
                    'cep': '29163-490',
                    'street': 'Rua Samora Machel',
                    'neighborhood': 'Cidade Continental-Setor África',
                    'city': 'Serra',
                    'state': 'ES',
                    'number': '12',
                    'description': 'Descrição da organização',
                    'category_name': 3,
                    'complement': ''
                },
                {
                    'name': 'Organização 4',
                    'email': 'org4@email.com',
                    'phone': '11968317891',
                    'cep': '69316-586',
                    'street': 'Rua Renato Marques Jr',
                    'neighborhood': 'Senador Hélio Campos',
                    'city': 'Boa Vista',
                    'state': 'RR',
                    'number': '710',
                    'description': 'Descrição da organização',
                    'category_name': 4,
                    'complement': ''
                },
                {
                    'name': 'Organização 5',
                    'email': 'org5@email.com',
                    'phone': '11968317891',
                    'cep': '74740-530',
                    'street': 'Rua 3',
                    'neighborhood': 'Jardim Brasil',
                    'city': 'Goiânia',
                    'state': 'GO',
                    'number': '238',
                    'description': 'Descrição da organização',
                    'category_name': 5,
                    'complement': ''
                },
                {
                    'name': 'Organização 6',
                    'email': 'org6@email.com',
                    'phone': '11968317891',
                    'cep': '03332-005',
                    'street': 'Praça Joana Lombello Malavazi',
                    'neighborhood': 'Cidade Mãe do Céu',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '1',
                    'description': '',
                    'category_name': 6,
                    'complement': ''
                },
                {
                    'name': 'Organização 7',
                    'email': 'org7@email.com',
                    'phone': '11968317891',
                    'cep': '05187-160',
                    'street': 'Rua Daniel Faria Gonçalvez',
                    'neighborhood': 'Jardim Ipanema (Zona Oeste)',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '1',
                    'description': '',
                    'category_name': 7,
                    'complement': ''
                },
                {
                    'name': 'Organização 8',
                    'email': 'org8@email.com',
                    'phone': '11968317891',
                    'cep': '03877-100',
                    'street': 'Rua Engenheiro Osvaldo Andreani',
                    'neighborhood': 'Rua Engenheiro Osvaldo Andreani',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '1',
                    'description': '',
                    'category_name': 8,
                    'complement': ''
                },
                {
                    'name': 'Organização 9',
                    'email': 'org9@email.com',
                    'phone': '11968317891',
                    'cep': '05756-260',
                    'street': 'Rua Cauaburi',
                    'neighborhood': 'Jardim Umarizal',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '1',
                    'description': '',
                    'category_name': 9,
                    'complement': ''
                },
                {
                    'name': 'Organização 10',
                    'email': 'org10@email.com',
                    'phone': '11968317891',
                    'cep': '03570-480',
                    'street': 'Rua Júlia Antonieta Tepedino Guerra',
                    'neighborhood': 'Parque Savoy City',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '1',
                    'description': '',
                    'category_name': 10,
                    'complement': ''
                },
                # {
                #     'name': 'Organização 11',
                #     'email': 'org11@email.com',
                #     'phone': '11968317891',
                #     'cep': '04506002',
                #     'street': 'Avenida Santo Amaro',
                #     'neighborhood': 'Vila Nova Conceição',
                #     'city': 'São Paulo',
                #     'state': 'SP',
                #     'number': '1',
                #     'description': '',
                #     'category_name': 10,
                #     'complement': ''
                # },
                # {
                #     'name': 'Organização 12',
                #     'email': 'org12@email.com',
                #     'phone': '11968317891',
                #     'cep': '03813220',
                #     'street': 'Rua Muru-Muru',
                #     'neighborhood': 'Jardim Matarazzo',
                #     'city': 'São Paulo',
                #     'state': 'SP',
                #     'number': '1',
                #     'description': '',
                #     'category_name': 10,
                #     'complement': ''
                # },
                # {
                #     'name': 'Organização 13',
                #     'email': 'org13@email.com',
                #     'phone': '11968317891',
                #     'cep': '04402060',
                #     'street': 'Rua Dulce Carneiro',
                #     'neighborhood': 'Vila Marari',
                #     'city': 'São Paulo',
                #     'state': 'SP',
                #     'number': '1',
                #     'description': '',
                #     'category_name': 10,
                #     'complement': ''
                # },
                # {
                #     'name': 'Organização 14',
                #     'email': 'org14@email.com',
                #     'phone': '11968317891',
                #     'cep': '04434220',
                #     'street': 'Rua Dionísio Lavranga',
                #     'neighborhood': 'Jardim Orly',
                #     'city': 'São Paulo',
                #     'state': 'SP',
                #     'number': '1',
                #     'description': '',
                #     'category_name': 10,
                #     'complement': ''
                # },
                # {
                #     'name': 'Organização 15',
                #     'email': 'org15@email.com',
                #     'phone': '11968317891',
                #     'cep': '04432000',
                #     'street': 'Avenida Eduardo Pereira Ramos',
                #     'neighborhood': 'Jardim São Jorge',
                #     'city': 'São Paulo',
                #     'state': 'SP',
                #     'number': '439',
                #     'description': '',
                #     'category_name': 10,
                #     'complement': ''
                # },
                {
                    'name': 'Organização 16',
                    'email': 'org16@email.com',
                    'phone': '11968317891',
                    'cep': '04434120',
                    'street': 'Rua Eliseu Borge',
                    'neighborhood': 'Morro Grande',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '183',
                    'description': '',
                    'category_name': 10,
                    'complement': ''
                },
                {
                    'name': 'Organização 17',
                    'email': 'org17@email.com',
                    'phone': '11968317891',
                    'cep': '06786090',
                    'street': 'Rua Samuel Arnold',
                    'neighborhood': 'Jardim Orly',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '596',
                    'description': '',
                    'category_name': 10,
                    'complement': ''
                },
                {
                    'name': 'Organização 18',
                    'email': 'org18@email.com',
                    'phone': '11968317891',
                    'cep': '04434150',
                    'street': 'Rua Germano Gottsfritz',
                    'neighborhood': 'Jardim Uberaba',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '290',
                    'description': '',
                    'category_name': 10,
                    'complement': ''
                },
                {
                    'name': 'Organização 19',
                    'email': 'org19@email.com',
                    'phone': '11968317891',
                    'cep': '04432170',
                    'street': 'Rua Peixoto de Melo Filho',
                    'neighborhood': 'Jardim São Jorge',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '181',
                    'description': '',
                    'category_name': 10,
                    'complement': ''
                },
                {
                    'name': 'Organização 20',
                    'email': 'org20@email.com',
                    'phone': '11968317891',
                    'cep': '04432100',
                    'street': 'Rua Doutor José Virgílio Vita',
                    'neighborhood': 'Jardim São Jorge',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'number': '16',
                    'description': '',
                    'category_name': 10,
                    'complement': ''
                }
                ]

            for org_data in orgs:
                if Organization.objects.filter(email=org_data['email']).exists():
                    continue

                # Crie a organização
                organization = Organization.objects.create(
                    name=org_data['name'],
                    email=org_data['email'],
                    phone=org_data['phone'],
                    cep=org_data['cep'],
                    street=org_data['street'],
                    neighborhood=org_data['neighborhood'],
                    city=org_data['city'],
                    state=org_data['state'],
                    number=org_data['number'],
                    complement=org_data['complement'],
                    description=org_data['description'],
                )
                
                organization.category.set([Category.objects.get(name=org_data['category_name'])])

                # Adicione o usuário
                admin_user = CustomUser.objects.get(email=admin_email)
                organization.users.add(admin_user)

                UserRole.objects.create(user=admin_user, organization=organization, role=0)

                # Obtenha os detalhes do local usando o Google Maps API
                address = f'{organization.street} {organization.number}, {organization.cep}, {organization.city} - {organization.state}'
                gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                location = gmap.geocode(address)[0]

                place_id = location.get('place_id', None)
                lat = location.get('geometry', {}).get('location', {}).get('lat', None)
                lng = location.get('geometry', {}).get('location', {}).get('lng', None)
                
                organization.lat = lat
                organization.lng = lng
                organization.place_id = place_id
                organization.save()
            
            self.stdout.write(self.style.SUCCESS('Objetos criados com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar os objetos!\n{e}'))

        
