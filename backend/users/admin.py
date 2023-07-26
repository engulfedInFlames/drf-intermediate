from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ...


admin.site.unregister(Group)
