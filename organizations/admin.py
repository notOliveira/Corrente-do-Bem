from django.contrib import admin
from .models import Organization, OrganizationProfile, Category

admin.site.register(Organization)
admin.site.register(OrganizationProfile)

@admin.register(Category)
class GenreAdmin(admin.ModelAdmin):    
    list_display = ["id", "name"]

