from django.contrib import admin
from .models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number', 'email')


admin.site.register(User, AccountAdmin)
