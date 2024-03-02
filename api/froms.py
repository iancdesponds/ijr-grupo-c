from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Informe um email válido.')

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')