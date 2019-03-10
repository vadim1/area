from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class AreaAppUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), 'email', 'password', 'last_login', 'date_joined')
        }),
        ('Access Limits', {
            'fields': ('access_override', 'access_counter', 'max_limit')
        }),
        ('Other Settings', {
            'fields': ('has_tou', 'is_active', 'is_staff', 'is_superuser')
        })
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'access_counter')
    ordering = ['first_name', 'last_name', 'email']
    readonly_fields = ('last_login', 'date_joined',)
    search_fields = ['first_name', 'last_name', 'email']

admin.site.register(User, AreaAppUserAdmin)