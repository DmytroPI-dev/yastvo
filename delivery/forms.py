from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import gettext as _

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class AddDishesForm(forms.Form):
    item = forms.CharField(required=True, widget=forms.TextInput(attrs=
    {'class':'form-control'

    }))
    
    pass





class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': _('First name'), 
    'id': 'firstName', 
     
    }))

    last_name =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
    'placeholder': _('Last name'),
    'id': 'lastName', 
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'email@email.com',
        'id': 'email',
        'type':'e-mail'

    }))
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Your address'),
        'id': 'address',
    }))

    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Apartment or suite'),
        'id':'address2',
    }))

    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder':'+1(235)45-89-89',
        'id':'phone-number'
    }))

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)
