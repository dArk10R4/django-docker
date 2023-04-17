from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import InstagramCredentials

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SigninForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    
class InstagramCredentialsForm(forms.ModelForm):
    instagram_username = forms.CharField(max_length=50)
    instagram_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = InstagramCredentials
        fields = ['instagram_username', 'instagram_password']