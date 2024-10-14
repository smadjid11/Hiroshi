from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username' : forms.TextInput(attrs={
                'name' : 'username',
                'class' : 'username',
                'id' : 'username',
            }),
            'password' : forms.PasswordInput(attrs={
                'name' : 'password',
                'class' : 'password',
                'id' : 'password',
            }),
        }

class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['title']
        widgets = {
            'title' : forms.TextInput(attrs={
                'name' : 'title',
                'class' : 'title',
                'id' : 'title',
                'style' : 'resize: none;',
            })
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'price', 'sizes')
        widgets = {
            'category' : forms.Select(attrs={
                'name' : 'category',
                'id' : 'category',
                'class' : 'category',
            }),
            'name' : forms.TextInput(attrs={
                'name' : 'name',
                'id' : 'name',
                'class' : 'name',
            }),
            'price' : forms.NumberInput(attrs={
                'name' : 'price',
                'id' : 'price',
                'class' : 'price',
                # 'min' : 1,
            }),
            'sizes' : forms.SelectMultiple(attrs={
                'name' : 'sizes',
                'id' : 'sizes',
                'class' : 'sizes',
            }),
        }

class UpdateSizesForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sizes']
        widgets = {
            'sizes' : forms.SelectMultiple(attrs={
                'name' : 'sizes',
                'class' : 'sizes',
                'id' : 'sizes',
            })
        }