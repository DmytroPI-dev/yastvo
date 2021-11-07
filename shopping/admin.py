from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class LunchAdminForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style = "color:red;"> Загружайте изображения с минимальным разрешением {} x {}</span>'
            .format(*Product.MIN_RESOLUTION))


    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не более 4 MB!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Размер изображения слишком маленький!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Размер изображения слишком большой!')    
        return image


class SaladAdminForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style = "color:red;"> Загружайте изображения с минимальным разрешением {} x {}</span>'
            .format(*Product.MIN_RESOLUTION))


    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не более 4 MB!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Размер изображения слишком маленький!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Размер изображения слишком большой!')    
        return image


class French_toastsAdminForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style = "color:red;"> Загружайте изображения с минимальным разрешением {} x {}</span>'
            .format(*Product.MIN_RESOLUTION))


    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не более 4 MB!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Размер изображения слишком маленький!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Размер изображения слишком большой!')    
        return image


class BreakfastAdminForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style = "color:red;"> Загружайте изображения с минимальным разрешением {} x {}</span>'
            .format(*Product.MIN_RESOLUTION))


    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не более 4 MB!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Размер изображения слишком маленький!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Размер изображения слишком большой!')    
        return image


class SnackAdminForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style = "color:red;"> Загружайте изображения с минимальным разрешением {} x {}</span>'
            .format(*Product.MIN_RESOLUTION))


    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не более 4 MB!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Размер изображения слишком маленький!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Размер изображения слишком большой!')    
        return image        


class BreakfastAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Breakfast'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SnackAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Snack'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    


class SaladAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Salads'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)   


class LunchAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Lunch'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)           


class French_toastsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='French_toasts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)   

admin.site.register(Category)
admin.site.register(Breakfast, BreakfastAdmin)
admin.site.register(Snack, SnackAdmin)
admin.site.register(French_toasts, French_toastsAdmin)
admin.site.register(Salads, SaladAdmin)
admin.site.register(Lunch, LunchAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

