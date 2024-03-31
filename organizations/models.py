from django.db import models
from PIL import Image
from .constants import STATE_CHOICES, CATEGORY_CHOICES
from users.models import CustomUser as User

class Category(models.Model):
    name = models.IntegerField(choices=CATEGORY_CHOICES, unique=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
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
    lat = models.CharField(max_length=200, null=True, blank=True)
    lng = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField('users.CustomUser', related_name='organization_users', blank=True)
    category = models.ManyToManyField(Category, related_name='organizations', blank=True)
    
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        
    def __str__(self):
        return self.name
    
class OrganizationProfile(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    image = models.ImageField(default='default_org_picture.png', upload_to='org_pics')
    website = models.CharField(blank=True, null=True, max_length=200)
    instagram = models.CharField(blank=True, null=True, max_length=50)
    
    class Meta:
        verbose_name = 'Organization Profile'
        verbose_name_plural = 'Organization Profiles'
        
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

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='donations_pics', blank=True, null=True)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        
    def __str__(self):
        return f'Doação #{self.id} - {self.user.username} - {self.organization.name}'