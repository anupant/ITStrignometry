__author__ = 'Anna'
from django.contrib.auth.models import User
from django import forms



#This class is for your user registration
class UserForm(forms.ModelForm):
    #This widget forms is written to hide the password information
    password = forms.CharField(widget = forms.PasswordInput)

    #information about your class
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



