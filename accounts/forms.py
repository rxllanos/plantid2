from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=15, required=False, help_text='Optional')
    profile_photo = forms.ImageField(required=False, help_text='Optional. Upload a profile photo.')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_photo', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass