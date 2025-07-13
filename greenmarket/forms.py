from django import forms  # ✅ correct
from django.contrib.auth.forms import AuthenticationForm
from .models import*
from django.core.exceptions import ValidationError

from django import forms  # ✅ correct
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User



class FarmerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_type = forms.ChoiceField(choices=[('farmer', 'Farmer'), ('buyer', 'Buyer')])
    email = forms.EmailField()
    pass1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    pass2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("pass1")
        password2 = cleaned_data.get("pass2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# product form

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = FarmProduct
        fields = '__all__'


