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


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


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


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Завтраки целый день': 'breakfast__count',
        'Сытный перекус': 'snack__count',
        'Обычно берут на обед': 'lunch__count',
        'Больше чем салат': 'salads__count',
        'Французские тосты': 'french_toasts__count',
        
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('breakfast', 'snack', 'lunch', 'salads', 'french_toasts')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url = c.get_absolute_url(), count=getattr(c,self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data
        
            
        
        

class Category (models.Model):

    name = models.CharField(max_length=255, verbose_name = 'Имя категории')
    slug = models.SlugField(unique = True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'  



class Product(models.Model):

    MIN_RESOLUTION = 1000
    MAX_RESOLUTION = 3000
    MAX_IMAGE_SIZE = 5000000

    
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name = 'Категория', on_delete = models.CASCADE)
    slug = models.SlugField(unique = True)
    title = models.CharField(max_length = 255, verbose_name = 'Название блюда')
    price = models.DecimalField(max_digits= 9, decimal_places = 2, verbose_name = 'Цена', default=100)
    composition = models.TextField('Состав (описание) блюда', max_length=250, default='Состав')
    weight = models.IntegerField(verbose_name='Масса нетто, гр.', default=100)
    calories = models.IntegerField(verbose_name='Калорийность, Ккал', default=100)
    milk_added = models.BooleanField(verbose_name='Есть ли молоко в составе', default=False)
    image = models.ImageField(verbose_name = 'Изображение блюда', upload_to='goods')
     

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

    class Meta:
        verbose_name = 'Товар для корзины'
        verbose_name_plural = 'Товары для корзины'     


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Покупатель', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'     


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    # orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'     


class Breakfast(Product):
    some = models.CharField(max_length=255, verbose_name = 'Прочие характеристики', null=True, blank=True)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    class Meta:
        verbose_name = 'Завтрак'
        verbose_name_plural = 'Завтраки'     

    
class Snack (Product):
    some_new = models.CharField(max_length=255, verbose_name = 'Еще характеристики', null=True, blank=True)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    class Meta:
        verbose_name = 'Перекус'
        verbose_name_plural = 'Перекусы' 


class Lunch (Product):
    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')   

    class Meta:
        verbose_name = 'Обед'
        verbose_name_plural = 'Обеды'      


class Salads (Product):
    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')   
        
    class Meta:
        verbose_name = 'Салат'
        verbose_name_plural = 'Салаты'         


class French_toasts (Product):
    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')            

    class Meta:
        verbose_name = 'Тост'
        verbose_name_plural = 'Тосты' 
