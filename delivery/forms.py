from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'First name', 
    'id': 'firstName', 
     
    }))

    last_name =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
    'placeholder': 'Last name',
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
        'placeholder': 'Mayflower Street',
        'id': 'address',
    }))

    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment or suite',
        'id':'address2',
    }))

    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder':'+1(235)45-89-89',
        'id':'phone-number'
    }))

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)
