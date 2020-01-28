from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CustomerForm(ModelForm):
  name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
  phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  
  class Meta:
    model = Customer
    fields = '__all__'
    exclude = ['user'] 


class OrderForm(ModelForm):
  class Meta:
    model = Order
    fields = '__all__'


class UserAuthForm(UserCreationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
  email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'someone@example.com', 'class':'form-control', 'type': 'email'}))
  password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Password', 'class':'form-control', 'type':'password'}))
  password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Confirm Password', 'class':'form-control', 'type':'password'}))
  class Meta:
    model = User
    fields =['username', 'email', 'password1', 'password2']