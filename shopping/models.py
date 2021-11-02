import sys
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone
from io import BytesIO


User = get_user_model()

def get_product_url(obj, viewname):
    ct_model = obj.__class__.meta.model_name
    return reverse (viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

    
# class MinResolutionErrorExeption(Exception):
#     pass

# class MaxResolutionErrorExeption(Exception):
#     pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class Category (models.Model):

    name = models.CharField(max_length=255, verbose_name = 'Имя категории')
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name

class Product(models.Model):

    MIN_RESOLUTION = (400,400)
    MAX_RESOLUTION = (3000,3000)
    MAX_IMAGE_SIZE = 4194304 

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name = 'Категория', on_delete = models.CASCADE)
    title = models.CharField(max_length = 255, verbose_name = 'Название товара')
    slug = models.SlugField(unique = True)
    image = models.ImageField(verbose_name = 'Изображение товара', upload_to='goods')
    description = models.TextField (verbose_name = 'Описание товара', null = True)
    price = models.DecimalField(max_digits= 9, decimal_places = 2, verbose_name = 'Цена')

    def __str__(self):
        return self.title
# A function to resize image to 600*600 pixels

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((600,600), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream,'JPEG', quality =90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile (
            filestream,'Imagefield', name, 'jpeg/image', sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)

# EOF #


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    # orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Grocery(Product):
    shelf_life = models.CharField(max_length=7, verbose_name='Срок хранения')
    net_weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Масса нетто')
    in_box = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Количество в упаковке')
    milk_added = models.BooleanField(verbose_name='Молоко в составе', default=False)
    fridge_life = models.CharField(max_length=10, verbose_name='Срок хранения в холодильнике', default=1)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
    
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


    
class Maindishes (Product):
    shelf_life = models.CharField(max_length=7, verbose_name='Срок хранения')
    net_weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Масса нетто')
    in_box = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Количество в упаковке', default=1)
    milk_added = models.BooleanField(verbose_name='Молоко в составе', default=False)
    fridge_life = models.CharField(max_length=10, verbose_name='Срок хранения в холодильнике')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')
    


