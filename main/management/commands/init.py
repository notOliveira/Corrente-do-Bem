from django.core.management.base import BaseCommand
from users.models import CustomUser
from organizations.models import Category
from organizations.constants import CATEGORY_CHOICES

class Command(BaseCommand):
    help = 'Cria os objetos padrão do banco'

    def handle(self, *args, **options):

        # Adiciona as categorias
        Category.objects.bulk_create([Category(name=value) for value, _ in CATEGORY_CHOICES if not Category.objects.filter(name=value).exists()])
        
        self.stdout.write(self.style.SUCCESS('Objetos criados com sucesso.'))
        
        # Criando superusuário
        if not CustomUser.objects.filter(email='admin@admin.com').exists():
            CustomUser.objects.create_superuser(
                email='admin@admin.com',
                username='admin@admin.com',
                first_name='Admin',
                last_name='Administrator',
                password='admin'
                )
                
