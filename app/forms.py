from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Products, Category, CustomerOrder, Custom

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'image']

class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ['status']

class customForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = ['Shoulder', 'Body_Length', 'Chest', 'Waist', 'Bottom_width',  'Sleeve_length', 'category']       






