from django.db import models


class Messages (models.Model):
    email = models.EmailField('Ваш Email:', max_length=50)
    subject = models.CharField('Тема письма', max_length=100)
    message = models.TextField('Ваше сообщение', max_length=1000)

    def __str__(self):
        return self.email