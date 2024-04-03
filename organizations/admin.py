from django.contrib import admin
from .models import Organization, OrganizationProfile, Category, Donation, UserRole

admin.site.register(Organization)
admin.site.register(OrganizationProfile)
admin.site.register(Donation)
admin.site.register(UserRole)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):    
    list_display = ["id", "name"]
