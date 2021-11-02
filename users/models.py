# from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Аватар пользователя', default='default.png', upload_to='avatars')
    name = models.CharField('Ваше имя', max_length=20, default='Веган')
    phone = models.CharField('Телефон пользователя', max_length=15)
    


    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

