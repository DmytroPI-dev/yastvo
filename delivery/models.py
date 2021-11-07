import sys
from PIL import Image
from io import BytesIO
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile


class MenuItems (models.Model):
    title = models.CharField('Название блюда', max_length=50, default='Наименование блюда')
    item_description = models.TextField('Описание блюда', max_length=250, default='Описание блюда')
    item_composition = models.TextField('Состав блюда', max_length=250, default='Состав')
    item_weight = models.IntegerField(verbose_name='Масса нетто')
    item_price = models.IntegerField(verbose_name='Цена блюда')
    item_calories = models.IntegerField(verbose_name='Калорийность', default=100)
    item_image = models.ImageField('Фотография блюда', upload_to='goods')
    milk_added = models.BooleanField(verbose_name='Молоко в составе', default=False)


    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        item_image = self.item_image
        img = Image.open(item_image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((600,600), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream,'JPEG', quality =90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.item_image.name.split('.'))
        self.item_image = InMemoryUploadedFile (
            filestream,'Imagefield', name, 'jpeg/image', sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)    

    def get_absolute_url(self):
        return reverse ('add')

