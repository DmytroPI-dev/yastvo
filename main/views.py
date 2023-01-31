from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _


def index(request):
    return render(request, 'main/index.html')


def menu(request):
    return render(request, 'main/menu.html')


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, _('Message sent'))
            form.save()
            subject = _('Message from site')
            body = {
                'email' : form.cleaned_data['email'],
                'subject' : form.cleaned_data['subject'],
                'message' : form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject=subject, message=message, from_email='demetriy.78@gmail.com', recipient_list=['demetriy.78@gmail.com'])
            except BadHeaderError:
                return HttpResponse(_('Incorrect header'))
            return redirect ('contacts')

    form = ContactForm()
    return render(request, "main/contacts.html", {'form': form})
