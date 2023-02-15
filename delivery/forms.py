from django import forms
from django.utils.translation import gettext as _
from .models import CATEGORY, LABEL, MenuItems

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class AddDishesForm(forms.ModelForm):
    item = forms.CharField(max_length=50, widget=forms.TextInput(attrs=
    {'class':'form-control',
    'placeholder':_('Item name'),
    'id':'menuItem'
    }))

    category = forms.ChoiceField(choices=CATEGORY,required=True, widget=forms.Select (attrs={
    'class':'form-control',
    'id':'category'
    }))

    label = forms.ChoiceField(choices=LABEL, required=False, widget=forms.Select (attrs={
    'class':'form-control',
    'id':'label'
    }))

    item_description = forms.CharField(widget=forms.TextInput (attrs=
    {'class':'form-control',
    'placeholder':_('Item description'),
    'id':'itemDescription'
    }))
    item_composition = forms.CharField(widget=forms.TextInput (attrs=
    {'class':'form-control',
    'placeholder':_('Item composition'),
    'id':'itemComposition'
    }))
    item_weight = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
    'class':'form-control',
    'id':'weight'
    }))

    item_price = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
    'class':'form-control',
    'id':'price'
    }))
    item_discount = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
    'class':'form-control',
    'id':'discount'
    }))
    item_calories = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
    'class':'form-control',
    'id':'calories'
    }))
    item_image = forms.ImageField(widget=forms.FileInput)
    milk_added =forms.CheckboxInput(attrs={
         'class':'form-control',
        'id':'milk'
    })

    class Meta:
        model = MenuItems
        fields = ['item', 'category', 'label', 'item_description','item_composition','item_weight','item_price','item_discount','item_calories', 'item_image', 'milk_added']



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
