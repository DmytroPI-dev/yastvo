from django.db import models
from django.utils.translation import gettext as _

class Messages (models.Model):
    email = models.EmailField(_("Your email address"), max_length=50)
    subject = models.CharField(_('Email subject'), max_length=100)
    message = models.TextField(_('Email text'), max_length=1000)

    def __str__(self):
        return self.email