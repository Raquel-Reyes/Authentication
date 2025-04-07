from django import forms
from .models import User
from .encriptacion import cryptPassword

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña', required=True)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

