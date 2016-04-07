from django.contrib import admin

# Register your models here.

from .models import MyUser

@admin.register(MyUser)
class ActivateUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_active', 'is_superuser']
    search_fields = ['first_name', 'username', 'email']
    actions_on_bottom = True
    date_hierarchy = 'date_joined'
