from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.translation import gettext as _


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(
        label=_('Enter Your email:'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter email address:')})
    )

    username = forms.CharField(
        label=_('Enter login'),
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter login')})
    )

    password1 = forms.CharField(
        label=_('Enter password'),
        required=True,
        help_text=_('The password must be not too short and not common'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter password')})
    )

    password2 = forms.CharField(
        label=_('Enter password again'),
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter password again')})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        label=_('Enter Your email:'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter Your email:')})
    )

    username = forms.CharField(
        label=_('Enter login'),
        required=False,
        help_text=_('Don`t use special characters'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter login')})
    )

    class Meta:
        model = User
        fields = ['username', 'email']



class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label=_('Upload Your photo'),
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    name = forms.CharField(
        label=_('Please, enter Your name'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Please, enter Your name')})
    )

    
    phone = forms.CharField(
        label=_('Phone'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone')})
    )


    class Meta:
        model = Profile
        fields = ['name', 'img', 'phone']




