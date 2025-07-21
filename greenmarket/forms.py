from django import forms
from django.contrib.auth.models import User
from .models import Product  # Or FarmProduct

# -------------------------------
# Registration Form
# -------------------------------
class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    user_type = forms.ChoiceField(
        choices=[('farmer', 'Farmer'), ('buyer', 'Buyer')],
        label="Registering As"
    )
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# -------------------------------
# Login Form
# -------------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# -------------------------------
# Product Form
# -------------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['farmer']