from django.contrib import admin
from .models import Organization, OrganizationProfile, Category, Donation

admin.site.register(Organization)
admin.site.register(OrganizationProfile)
admin.site.register(Donation)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):    
    list_display = ["id", "name"]

