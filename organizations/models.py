from django.db import models
from PIL import Image
from .constants import STATE_CHOICES, CATEGORY_CHOICES

class Category(models.Model):
    name = models.IntegerField(choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Organization(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, blank=True)
    cep = models.CharField(max_length=9, blank=True)
    street = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)
    number = models.CharField(max_length=10, blank=True)
    complement = models.CharField(max_length=50, blank=True)
    place_id = models.TextField(null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField('users.CustomUser', related_name='organization_users', blank=True)
    category = models.ManyToManyField(Category, related_name='organizations', blank=True)

    def __str__(self):
        return self.name

class OrganizationProfile(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    image = models.ImageField(default='default_org_picture.png', upload_to='org_pics')
    website = models.CharField(blank=True, null=True, max_length=200)
    instagram = models.CharField(blank=True, null=True, max_length=50)
    
    def __str__(self):
        return f'{self.organization.name} - Profile'
    
    # Substituindo método save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 1000 or img.width > 1000:
            output_size = (1000, 1000)
            img.thumbnail(output_size)
            img.save(self.image.path)
