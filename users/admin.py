from django.contrib import admin
from .models import Profile, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'get_organizations_name', 'cep', 'is_active', 'is_staff']
    search_fields = ('email', 'organizations')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    def get_organizations_name(self, obj):
        return ", ".join([organizations.name for organizations in obj.organizations.all()])
    
    get_organizations_name.short_description = 'Organizations'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    search_fields = ('user', 'image')
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()