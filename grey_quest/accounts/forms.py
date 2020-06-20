from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
import re

def validate_special_Character(word):
    for char in word:
        if not char.isdigit() and not char.isalpha():
            return False
    return True


class LoginForm(forms.Form):
    username = forms.CharField(label="Enter user name",widget=forms.TextInput(attrs={'class':"form-control",}))
    pwd = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':"form-control",}))
    remember_me = forms.BooleanField(required=False)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Enter user name",widget=forms.TextInput(attrs={'class':"form-control",}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-control",}))
    pwd = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':"form-control",}))
    cpwd = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':"form-control",}))
    


    def clean_username(self):
        if not validate_special_Character(self.cleaned_data.get('username')):
            raise forms.ValidationError("Usernames contains characters that are not numbers nor letters")
        if User.objects.filter(username__iexact=self.cleaned_data.get('username')).exists():
            raise ValidationError("Username already exists.")
        return self.cleaned_data.get('username')

    def clean(self):
        data = self.cleaned_data
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data.get('pwd')):
            raise ValidationError("The password must contain at least 1 symbol: " +"!@#$%<,.;")
        if not re.findall('[A-Z]', data.get('pwd')):
            raise ValidationError("The password must contain at least 1 capital letter")

        if len(data.get('pwd'))<=8:
            raise ValidationError("Password too small")
        if data.get('pwd')==data.get('cpwd'):
            return data

        else:
            raise ValidationError("Password's doesn't match")
    