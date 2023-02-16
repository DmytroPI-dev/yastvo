from modeltranslation.translator import translator, TranslationOptions
from .models import MenuItems


class NewTranslationOptions (TranslationOptions):
    fields = ('item', 'item_description', 'item_composition')


translator.register(MenuItems, NewTranslationOptions)