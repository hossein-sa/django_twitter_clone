from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'bio', 'is_staff', 'is_active')


admin.site.register(CustomUser, CustomUserAdmin)
