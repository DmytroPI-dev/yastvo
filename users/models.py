# from typing_extensions import Required
from django.core.files.base import BytesIO, ContentFile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.translation import gettext as _


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(
        _('User avatar'), default='avatars/default.png', upload_to='avatars')
    name = models.CharField(_('Your name:'), max_length=20, default=_('Vegan'))
    phone = models.CharField(_('Your phone:'), max_length=15)

    def save(self, *args, **kwargs):
        if self.img:
            image = Image.open(self.img)
            if image.height > 256 or image.width > 256:
                resize = (256, 256)
                image.thumbnail(resize)
                temp_file = BytesIO()
                image.save(temp_file, format=image.format)
                temp_file.seek(0)
                self.img.save(self.img.name, ContentFile(temp_file.read()), save=False)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'_("User profile") {self.user.username}'
