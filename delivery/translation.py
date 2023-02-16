from .models import MenuItems
from modeltranslation.translator import translator, TranslationOptions


class NewTranslationOptions (TranslationOptions):
    fields = ('item', 'item_description', 'item_composition')


translator.register (MenuItems, NewTranslationOptions)