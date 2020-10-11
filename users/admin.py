from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserModel, CustomAdminModel
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserModel
    form =  CustomAdminModel
    model = CustomUser
    list_display = ['username', 'email', 'age', 'is_staff']

admin.site.register(CustomUser,CustomUserAdmin)
