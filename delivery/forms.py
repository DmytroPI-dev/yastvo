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
        'id': 'email'

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

    country = CountryField(blank_label='(select country)').formfield( widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100 form-control',
        'id':'country'
    }))
    
    zip = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip',
        'placeholder': '00-100'
    }))

    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)
