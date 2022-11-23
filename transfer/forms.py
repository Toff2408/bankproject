from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Signupform(UserCreationForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    Last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)

    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone','password1','password2')