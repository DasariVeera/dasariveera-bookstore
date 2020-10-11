from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserModel(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'email', 'password1', 'password2']

class CustomAdminModel(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields