from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
      ('Extra Fields', {'fields': ('user_img',)}),
    )

# Register your models here.
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Freelancer)
admin.site.register(Employer)
