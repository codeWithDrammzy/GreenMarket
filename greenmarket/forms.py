from django import forms  # ✅ correct
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CreatefarmerForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        username = forms.CharField( max_length=20, required=False)
        password = forms.CharField( max_length=20, required=False)
