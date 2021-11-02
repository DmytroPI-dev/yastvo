from django.db import models
from django import forms
from django.forms import widgets
from .models import Messages

class ContactForm(forms.ModelForm):

    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea,max_length=1000, label="Ваше сообщение:")

    class Meta:
        model = Messages
        fields = ['email', 'subject', 'message']