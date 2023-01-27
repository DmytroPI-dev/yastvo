from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(
        label='Введите Email:',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )

    username = forms.CharField(
        label='Введите логин:',
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )

    password1 = forms.CharField(
        label='Введите пароль:',
        required=True,
        help_text='Пароль не должен быть коротким и слишком простым.',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

    password2 = forms.CharField(
        label='Подтвердите пароль:',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторно введите пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        label='Введите Email:',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'})
    )

    username = forms.CharField(
        label='Введите логин:',
        required=False,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']



class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Загрузите Ваше фото',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    name = forms.CharField(
        label='Укажите Ваше имя',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Укажите Ваше имя'})
    )

    
    phone = forms.CharField(
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'})
    )


    class Meta:
        model = Profile
        fields = ['name', 'img', 'phone']




